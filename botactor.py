from gameinfo import GameData
from wordset import WordSet, findRandomComplexWord
from common import buidUserReplayKeyboad, buildKeyboard

import data
import text
import logger

import numpy as np
import math
import time

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

def buildBotWordLenKeyboad(wordLen: int):
    return buildKeyboard(
        [
            ([["меньше чем " + str(wordLen), "word_len_dec"]] if wordLen > data.wordLenMin else []) 
              + [[str(wordLen) + " букв(ы)", "word_len_match"]] 
              + ([["больше чем " + str(wordLen), "word_len_inc"]] 
                    if wordLen < data.wordsByLen.size - 1 else []),
            map(lambda i: ["?", "char_" + str(i)], range(wordLen)),
            [["Выбери число букв сам", "word_len_random"]]
        ]
    )


async def chooseBotWordLen(userMsg: Message, gd: GameData):
    bd = gd.botData

    gd.setChatText(text.botWord.format(userName=gd.userName))
    gd.setChatMarkup(buildBotWordLenKeyboad(bd.wordLen))
    await gd.redrawAll(userMsg)

@router.callback_query(StateFilter("choiseActor"),  
                       F.data.in_(["bot_actor"]))
async def bot_word(callback: types.CallbackQuery, state: FSMContext):
    gd = (await state.get_data())["gameData"]
    bd = gd.botData
    bd.wordLen = data.startBotWordLen

    bd.resolvedChars = None # Don't draw botGameState 

    await chooseBotWordLen(callback.message, gd)

    await state.set_state("botWordLen")

@router.callback_query(StateFilter("botWordLen"),  F.data.in_(["word_len_dec", "word_len_inc"]))
async def bot_word_len_change(callback: types.CallbackQuery, state: FSMContext):
    gd = (await state.get_data())["gameData"]
    bd = gd.botData
    if callback.data == "word_len_dec":
        bd.wordLen -= 1
    else:
        assert callback.data == "word_len_inc"
        bd.wordLen += 1
    await chooseBotWordLen(callback.message, gd)

@router.callback_query(StateFilter("botWordLen"), F.data.in_(["word_len_match", "word_len_random"]))
async def bot_word_len_match(callback: types.CallbackQuery, state: FSMContext):
    gd = (await state.get_data())["gameData"]
    bd = gd.botData

    if callback.data == "word_len_random":
        bd.wordLen = math.floor(data.botWordLenMin 
                                + (data.botWordLenMax + 1 - data.botWordLenMin) 
                                    * np.random.random_sample())

    bd.resolvedChars = ["?"] * bd.wordLen
    bd.successChars  = []
    bd.failedChars   = []

    gd.setChatText("Подбираю слово ...")
    gd.setChatMarkup(None)

    await gd.redrawAll(callback.message)

    redrawMoment:float = 0.0
    async def showProgress(percent: int) -> None:
        nonlocal redrawMoment
        gd.setChatText(text.botRandomWord.format(wordLen=bd.wordLen, percent=percent))
        moment:float = time.time()
        if moment - redrawMoment > 0.5:
            await gd.redrawAll(callback.message)
            redrawMoment = moment      

    bd.guessedWord   = await findRandomComplexWord(bd.wordLen, showProgress)

    logger.put(text.logBotGuessWord.format(guessedWord=bd.guessedWord))

    gd.setChatText(text.botGuessStart.format(wordLen=bd.wordLen))

    await gd.redrawAll(callback.message)

    await state.set_state("botCharGuess")



