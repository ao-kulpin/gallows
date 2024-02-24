import asyncio
import logging
import numpy as np
import numpy.typing as npt

from contextlib import suppress
from random import randint
from typing import Optional

from gameinfo import GameData
from wordset import WordSet
import text
import char
import data
import filter
import gmessage as gm
import logger
import useractor

from aiogram import Bot, Dispatcher, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config_reader import config

RussNounsFN = "russian_nouns_without_filter.txt"  #####"russian_nouns.txt"

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()
dp.include_router(useractor.router)
logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    gd = GameData(userName=message.from_user.first_name)
    ud = gd.userData
    ud._picNum = 0 ##############################
    await state.set_data({"gameData": gd})
    ###print(f"start: gd({gd}) ud({ud})")
    gd.setHeadPhoto("splash.jpg")
    #############gd.setHeadText("Картинка " + str(ud._picNum)) #############
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Я задумал(а) слово", callback_data="user_word"))
    builder.row(types.InlineKeyboardButton(text="Пошел в ... c такими играми", callback_data="user_away"))

    gd.setChatText(text.userGreet.format(userName=gd.userName))
    gd.setChatMarkup(builder.as_markup())
    await gd.redrawAll(message)

    logger.put(text.logUserStart.format(firstName=message.from_user.first_name, lastName=message.from_user.last_name))

    await state.set_state("userStart")

@dp.callback_query(StateFilter("userStart", "userBotWin", "userUnknownWord", "userWin"),  F.data.in_(["user_away", "noreplay"]))
async def user_away(callback: types.CallbackQuery, state: FSMContext):
    gd = (await state.get_data())["gameData"]
    ud = gd.userData

    gd.setChatText(text.userAway.format(userName=gd.userName))

    gd.setChatMarkup(None)
    await gd.redrawAll(callback.message)

    logger.put(text.logUserAway.format(userName=gd.userName))

    await state.set_state("userAway")

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

