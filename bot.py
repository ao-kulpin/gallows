import asyncio
import logging
import numpy as np
import numpy.typing as npt
import signal

from contextlib import suppress
from random import randint
from typing import Optional

from gameinfo import GameData
from wordset import WordSet
from common import buildKeyboard

import text
import char
import data
import filter
import gmessage as gm
import logger
import useractor
import botactor
import sys
import argparse

from aiogram import Bot, Dispatcher, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.client.session.aiohttp import AiohttpSession

from config_reader import config


print(f"args: {sys.argv}")
bot = None  # the bot object
dp = None   # the dispatcher

async def createBot():    
    global bot
    global dp

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--proxy", help="use Pythonanywhere proxy server", 
                        action="store_true")
    args = parser.parse_args()

    print("Bot Gallows starting...")

    if args.proxy:
        # use the proxy server
        proxyURL = "http://proxy.server:3128"
        session  = AiohttpSession(proxy=proxyURL)
        bot = Bot(token=config.bot_token.get_secret_value(), session=session)
        print(f"using proxy {proxyURL}")
    else:
        # start without a proxy
        bot = Bot(token=config.bot_token.get_secret_value())

    dp = Dispatcher()
    dp.include_routers(useractor.router, botactor.router)
    logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    asyncio.run(createBot())

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    gd = GameData(userName=message.from_user.first_name)
    ud = gd.userData
    await state.set_data({"gameData": gd})
    gd.setHeadPhoto("splash.jpg")
    gd.setHeadText(text.introduction.format(userName=gd.userName, failureNumber=data.failureNumber))
    gd.setChatText(text.userInvite)
    gd.setChatMarkup(buildKeyboard(
        [
            [["Да, самое время поиграть", "choise_actor"]],
            [["Нет, играть с незнакомыми ботами опасно", "user_away"]]
        ]))
    await gd.redrawAll(message)

    logger.put(text.logUserStart.format(firstName=message.from_user.first_name, lastName=message.from_user.last_name))

    await state.set_state("userStart")

@dp.callback_query(StateFilter("userStart", "userUserWin", "userBotWin",
                               "botUserWin", "botBotWin", "userUnknownWord"),  
                   F.data.in_(["choise_actor", "replay"]))
async def choise_actor(callback: types.CallbackQuery, state: FSMContext):
    gd = (await state.get_data())["gameData"]
    gd.setHeadPhoto("splash.jpg")
    gd.setHeadText("")
    gd.setChatText(text.choiseActor.format(userName=gd.userName))
    gd.setChatMarkup(buildKeyboard(
        [
            [[f"Загадаю я ({gd.userName})", "user_actor"]],
            [["Загдывай ты (бот)", "bot_actor"]]
        ]))
    await gd.redrawAll(callback.message)

    await state.set_state("choiseActor")

async def botExit(message: types.Message, state: FSMContext) -> None:
    gd = (await state.get_data())["gameData"]
    ud = gd.userData

    gd.setChatText(text.userAway.format(userName=gd.userName))

    gd.setHeadText("")
    gd.setHeadPhoto("splash.jpg")

    gd.setChatMarkup(None)
    await gd.redrawAll(message)

    logger.put(text.logUserAway.format(userName=gd.userName))

    await state.set_state("userAway")

@dp.message(Command("exit"))
async def cmd_exit(message: types.Message, state: FSMContext):
    gd = GameData(userName=message.from_user.first_name)
    ud = gd.userData
    await state.set_data({"gameData": gd})
    await botExit(message, state)
    

@dp.callback_query(StateFilter("userStart", "userBotWin", "userUserWin", "userUnknownWord", 
                               "botUserWin", "botBotWin"),  
                  F.data.in_(["user_away", "noreplay"]))
async def user_away(callback: types.CallbackQuery, state: FSMContext):
    await botExit(callback.message, state)

async def createBot():    
    global bot
    global dp

    print("Bot Gallows starting...")
    proxyURL= 'http://proxy.server:3128'
    #session = AiohttpSession(proxy=proxyURL)
    #bot = Bot(token=config.bot_token.get_secret_value(), session=session)
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.include_routers(useractor.router, botactor.router)
    logging.basicConfig(level=logging.INFO)

# Start the bot
async def main():
    data.loadDictionary()

    logger.put(text.logBotStart.format(wordCount = data.allRussWords.size))

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, handle_as_tasks=True)

class TermException(Exception):
    def __init__(self, sigNum: int) :
        self.sigNum = sigNum

def terminateBot(sigNum: int, stack):
    raise TermException(sigNum)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, terminateBot)
    signal.signal(signal.SIGTERM, terminateBot)

    try:
        asyncio.run(main())
    except TermException as te:
        logger.put(text.logBotExit.format(sigNum=te.sigNum))
        logger.close()        

