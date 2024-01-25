import asyncio
import logging
import numpy as np
import numpy.typing as npt

from contextlib import suppress
from random import randint
from typing import Optional

from gameinfo import GameData
import text

from aiogram import Bot, Dispatcher, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from config_reader import config

RussNounsFN = "russian_nouns.txt"

allRussWords: npt.ArrayLike = None
wordLenMax = 100
wordLenMin = 2
wordsByLen = npt.ArrayLike = None
startUserWordLen = 6

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    gd = GameData(userName=message.from_user.first_name)
    ud = gd.userData
    await state.set_data({"gameData": gd})
    print(f"start: gd({gd}) ud({ud})")
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Я задумал(а) слово", callback_data="user_word"))
    builder.row(types.InlineKeyboardButton(text="Пошел в ... c такими играми", callback_data="user_away"))

    ud.startMsg = await message.answer(text.userGreet.format(userName=gd.userName), parse_mode="html", reply_markup=builder.as_markup())
    await state.set_state("userStart")

@dp.callback_query(StateFilter("userStart"),  F.data == "user_away")
async def user_away(callback: types.CallbackQuery, state: FSMContext):
    gd = (await state.get_data())["gameData"]
    ud = gd.userData
    await ud.startMsg.delete()
    await callback.message.answer(text.userAway.format(userName=gd.userName), parse_mode="html")
    await state.set_state("userAway")

def buidUserWordLenKeyboad(wordLen: int):
    global wordsByLen
    builder = InlineKeyboardBuilder()

    lenKeys = []
    if wordLen > wordLenMin:
        lenKeys.append(types.InlineKeyboardButton(text="меньше чем " + str(wordLen), callback_data=("word_len_dec")))
                       
    lenKeys.append(types.InlineKeyboardButton(text=str(wordLen) + " букв(ы)", callback_data=("word_len_exact")))

    if wordLen < wordsByLen.size - 1:
        lenKeys.append(types.InlineKeyboardButton(text="больше чем " + str(wordLen), callback_data=("word_len_inc")))
    builder.row(*lenKeys)

    charKeys = []
    for i in range(wordLen):
        charKeys.append(
            types.InlineKeyboardButton(text="?", callback_data=("char_" + str(i)))
        )
    builder.row(*charKeys)

    return builder.as_markup()        

async def updateUserWordLenMsg(gd: GameData):
    ud = gd.userData
    await ud.wordLenMsg.edit_text(text.userWord.format(userName=gd.userName), parse_mode="html", 
                                  reply_markup=buidUserWordLenKeyboad(ud.wordLen))


@dp.callback_query(StateFilter("userStart"),  F.data == "user_word")
async def user_word(callback: types.CallbackQuery, state: FSMContext):
    gd = (await state.get_data())["gameData"]
    ud = gd.userData
    ud.wordLen = startUserWordLen
    await ud.startMsg.delete()
    ud.wordLenMsg = await callback.message.answer(text.userWord.format(userName=gd.userName), parse_mode="html", 
                                  reply_markup=buidUserWordLenKeyboad(ud.wordLen))
    await state.set_state("userWordLen")

@dp.callback_query(StateFilter("userWordLen"),  F.data == "word_len_dec")
async def user_word_len_dec(callback: types.CallbackQuery, state: FSMContext):
    gd = (await state.get_data())["gameData"]
    ud = gd.userData
    ud.wordLen -= 1
    await updateUserWordLenMsg(gd)

@dp.callback_query(StateFilter("userWordLen"),  F.data == "word_len_inc")
async def user_word_len_dec(callback: types.CallbackQuery, state: FSMContext):
    gd = (await state.get_data())["gameData"]
    ud = gd.userData
    ud.wordLen += 1
    await updateUserWordLenMsg(gd)

@dp.callback_query(StateFilter("userWordLen"),  F.data == "word_len_exact")
async def user_word_len_exact(callback: types.CallbackQuery, state: FSMContext):
    gd = (await state.get_data())["gameData"]
    ud = gd.userData

    await ud.wordLenMsg.delete()

    ud.charGuessMsg = await callback.message.answer(text.userCharGuess.format(wordLen=ud.wordLen), parse_mode="html")

    await state.set_state("userCharGuess")


# Start the bot
async def main():
    global allRussWords
    global wordsByLen
    print("Bot Gallows starting...")
    print("Russian words loading...")
    allLines: list[str]
    try:
        f = open(RussNounsFN, "r", encoding='utf-8')
        allLines = np.array(f.readlines(), str)
        f.close()
    except:
        print(f"Can't load file {RussNounsFN}")
        return
    
    print(f"File {RussNounsFN} is loaded")
    allRussWords = np.empty(allLines.size, dtype=object)
    wordCount = 0
    actualLenMax = 0
    actualLenMin = 100
    wordLens = np.zeros(wordLenMax + 1, dtype=int)
    for line in allLines:
        word = line[:-1].upper()
        ### print(f"word:{word}")
        allRussWords[wordCount] = word
        lw = len(word)
        wordLens[lw] +=1
        if actualLenMax < lw: actualLenMax = lw
        if actualLenMin > lw: actualLenMin = lw
        wordCount += 1
        ### print(f"words: {allRussWords}")        

    wordsByLen = np.empty(actualLenMax + 1, dtype=object)
    for wl in range(actualLenMax + 1):
        wordsByLen[wl] = np.empty(wordLens[wl], dtype=int)

    wordLenCounts = np.zeros(actualLenMax + 1, dtype=int) 

    for wi in range(allRussWords.size):
        wl: int = len(allRussWords[wi])
        ### print(f"wi {wi}/{allRussWords[wi]}")
        wlc: int = wordLenCounts[wl]
        wordsByLen[wl][wlc] = wi
        wordLenCounts[wl] += 1

    ### for wli in range(wordsByLen.size):
    ###    print(f"wli({wli}:{wordsByLen[wli].size})->{[allRussWords[i] for i in wordsByLen[wli]]}")
    
    ### for i in range(wordLenMax):    
    ###  print(f"{i}: {wordLens[i]}")  

    print(f"{str(allRussWords.size)} words are loaded")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

