import asyncio
import logging
import numpy as np
import numpy.typing as npt

from contextlib import suppress
from random import randint
from typing import Optional

from gameinfo import GameData
import text
import char
import data
import filter

from aiogram import Bot, Dispatcher, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from config_reader import config

RussNounsFN = "russian_nouns.txt"

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

@dp.callback_query(StateFilter("userStart"),  F.data == "user_word")
async def user_word(callback: types.CallbackQuery, state: FSMContext):
    gd = (await state.get_data())["gameData"]
    ud = gd.userData
    ud.wordLen = data.startUserWordLen
    mstr = text.userWord.format(userName=gd.userName)
    print(mstr)
    ud.wordLenMsg = await (callback.message.answer(mstr, parse_mode="html", 
                                  reply_markup=buidUserWordLenKeyboad(ud.wordLen)))
    await ud.startMsg.delete()
    await state.set_state("userWordLen")


@dp.callback_query(StateFilter("userStart"),  F.data == "user_away")
async def user_away(callback: types.CallbackQuery, state: FSMContext):
    gd = (await state.get_data())["gameData"]
    ud = gd.userData
    await (callback.message.answer(text.userAway.format(userName=gd.userName), parse_mode="html", reply_markup=buidUserWordLenKeyboad(10)))
    await ud.startMsg.delete()
    await state.set_state("userAway")

def buidUserWordLenKeyboad(wordLen: int):
    builder = InlineKeyboardBuilder()

    lenKeys = []
    if wordLen > data.wordLenMin:
        lenKeys.append(types.InlineKeyboardButton(text="меньше чем " + str(wordLen), callback_data="word_len_dec"))
                       
    lenKeys.append(types.InlineKeyboardButton(text=str(wordLen) + " букв(ы)", callback_data="word_len_exact"))

    if wordLen < data.wordsByLen.size - 1:
        lenKeys.append(types.InlineKeyboardButton(text="больше чем " + str(wordLen), callback_data="word_len_inc"))
    builder.row(*lenKeys)

    charKeys = []
    for i in range(wordLen):
        charKeys.append(
            types.InlineKeyboardButton(text="?", callback_data=("char_" + str(i)))
        )
    builder.row(*charKeys)

    return builder.as_markup()        

def buidUserGuessCharKeyboad(resolvedChars: list[str], guessedChar: str, firstTry: bool = True):
    builder = InlineKeyboardBuilder()
    charKeys = []
    for i in range(len(resolvedChars)):
        charKeys.append(
            types.InlineKeyboardButton(text=resolvedChars[i], callback_data=("char_" + str(i)))
        )
    builder.row(*charKeys)
    builder.row(types.InlineKeyboardButton(text=("Нет буквы " if firstTry else "Больше нет букв ") 
                                                 + guessedChar + " в моем слове", 
                                           callback_data="nochar"))
    return builder.as_markup()

async def updateUserWordLenMsg(gd: GameData):
    ud = gd.userData
    await ud.wordLenMsg.edit_text(text.userWord.format(userName=gd.userName), parse_mode="html", 
                                  reply_markup=buidUserWordLenKeyboad(ud.wordLen))


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

    ud.resolvedChars = ["?"] * ud.wordLen

    ud.candidates = data.wordsByLen[ud.wordLen].copy()
    print(f"candidates: {ud.candidates}")
    counter = char.CharCounter()
    counter.countWords(ud.candidates, ud.resolvedChars)

    ud.guessedChar = counter.getMaxChar()

    ud.charCount = 0

    ud.charGuessMsg = await (callback.message.answer(
                                text.userCharGuess.format(wordLen=ud.wordLen, guessedChar=ud.guessedChar), 
                                parse_mode="html",
                                reply_markup=buidUserGuessCharKeyboad(ud.resolvedChars, 
                                                                      guessedChar=ud.guessedChar, 
                                                                      firstTry=True)))

    await ud.wordLenMsg.delete()
    await state.set_state("userCharGuess")

@dp.callback_query(StateFilter("userCharGuess"),  F.data == "nochar")
async def user_no_char(callback: types.CallbackQuery, state: FSMContext):
    gd = (await state.get_data())["gameData"]
    ud = gd.userData

    if ud.charCount == 0:
        ncf = filter.NoCharFilter(ud.guessedChar)
        ud.candidates = ncf.applyToWords(ud.candidates)
        failedChar = ud.guessedChar
        counter = char.CharCounter()
        counter.countWords(ud.candidates, ud.resolvedChars)

        ud.guessedChar = counter.getMaxChar()

        await ud.charGuessMsg.edit_text(
                                text.userFailedGuess.format(
                                    failedChar=failedChar, guessedChar=ud.guessedChar), 
                                parse_mode="html",
                                reply_markup=buidUserGuessCharKeyboad(ud.resolvedChars, 
                                                                      guessedChar=ud.guessedChar, 
                                                                      firstTry=True))
    else:
        cf = filter.CharFilter(ud.guessedChar, ud.resolvedChars)
        print(f"****** ResolvedChrs1: {ud.resolvedChars} candidates {ud.candidates.size}")
        print([data.allRussWords[i] for i in ud.candidates])
        ud.candidates = cf.applyToWords(ud.candidates)
        failedChar = ud.guessedChar
        counter = char.CharCounter()
        counter.countWords(ud.candidates, ud.resolvedChars)

        ud.guessedChar = counter.getMaxChar()
        print(f"****** ResolvedChrs2: {ud.resolvedChars} candidates {ud.candidates.size} char {ud.guessedChar}")
        print([data.allRussWords[i] for i in ud.candidates])

        ud.charCount = 0
        await ud.charGuessMsg.edit_text(
                                text.userCharGuess.format(wordLen=ud.wordLen, guessedChar=ud.guessedChar), 
                                parse_mode="html",
                                reply_markup=buidUserGuessCharKeyboad(ud.resolvedChars, 
                                                                      guessedChar=ud.guessedChar, 
                                                                      firstTry=(ud.charCount == 0)))

@dp.callback_query(StateFilter("userCharGuess"), F.data.startswith("char_"))
async def user_open_char(callback: types.CallbackQuery, state: FSMContext):
    gd = (await state.get_data())["gameData"]
    ud = gd.userData
    charPos = int(callback.data.split("_")[1])

    curChar = ud.resolvedChars[charPos]

    if curChar == "?":
        ud.resolvedChars[charPos] = ud.guessedChar
        ud.charCount += 1
    elif curChar == ud.guessedChar:        
        ud.resolvedChars[charPos] = "?"
        ud.charCount -= 1

    await ud.charGuessMsg.edit_text(
                                text.userCharGuess.format(wordLen=ud.wordLen, guessedChar=ud.guessedChar), 
                                parse_mode="html",
                                reply_markup=buidUserGuessCharKeyboad(ud.resolvedChars, 
                                                                      guessedChar=ud.guessedChar, 
                                                                      firstTry=(ud.charCount == 0)))



# Start the bot
async def main():
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
    data.allRussWords = np.empty(allLines.size, dtype=object)
    wordCount = 0
    actualLenMax = 0
    actualLenMin = 100
    wordLens = np.zeros(data.wordLenMax + 1, dtype=int)
    for line in allLines:
        word = line[:-1].upper()
        ### print(f"word:{word}")
        data.allRussWords[wordCount] = word
        lw = len(word)
        wordLens[lw] +=1
        if actualLenMax < lw: actualLenMax = lw
        if actualLenMin > lw: actualLenMin = lw
        wordCount += 1
        ### print(f"words: {data.allRussWords}")        

    data.wordsByLen = np.empty(actualLenMax + 1, dtype=object)
    for wl in range(actualLenMax + 1):
        data.wordsByLen[wl] = np.empty(wordLens[wl], dtype=int)

    wordLenCounts = np.zeros(actualLenMax + 1, dtype=int) 

    for wi in range(data.allRussWords.size):
        wl: int = len(data.allRussWords[wi])
        ### print(f"wi {wi}/{data.allRussWords[wi]}")
        wlc: int = wordLenCounts[wl]
        data.wordsByLen[wl][wlc] = wi
        wordLenCounts[wl] += 1

    ### for wli in range(data.wordsByLen.size):
    ###    print(f"wli({wli}:{data.wordsByLen[wli].size})->{[adata.llRussWords[i] for i in data.wordsByLen[wli]]}")
    
    ### for i in range(data.wordLenMax):    
    ###  print(f"{i}: {wordLens[i]}")  

    print(f"{str(data.allRussWords.size)} words are loaded")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, handle_as_tasks=False)


if __name__ == "__main__":
    asyncio.run(main())

