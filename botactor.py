from gameinfo import GameData
from wordset import WordSet, findRandomComplexWord
from common import buidUserReplayKeyboad, buildKeyboard

import data
import text
import logger
import char

import asyncio
import numpy as np
import math
import time

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

router = Router()

def buildBoutUntestedKeyboard(untestedChars: list[str]) -> InlineKeyboardMarkup:
    return buildKeyboard(
        [
            map(lambda ch_ind: [ch_ind[0], "char_" + str(ch_ind[1])], 
                zip(untestedChars, range(len(untestedChars))))
        ]
    )


def buildBotWordLenKeyboad(wordLen: int) -> InlineKeyboardMarkup:
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

async def drawBotGameState(state: FSMContext) -> None:
    gd = (await state.get_data())["gameData"]
    bd = gd.botData
    if bd.resolvedChars == None:
        # current game state is empty
        gd.setHeadText("")
    else:
        unresolveCount = bd.resolvedChars.count("?")
        successCount=len(bd.resolvedChars) - unresolveCount

        successCharsStr = ""
        for sc in bd.successChars:
            if successCharsStr != "":
                successCharsStr += ", "
            successCharsStr += sc
            scCount = bd.resolvedChars.count(sc)    
            assert scCount >= 1
            if scCount > 1:
                successCharsStr += f"({scCount})"

        failureRemain = data.failureNumber-len(bd.failedChars)

        gd.setHeadText(text.botGameState.format(resolvedChars=(" ".join(bd.resolvedChars)), wordLen=bd.wordLen,
                   failedCount=len(bd.failedChars), failedChars=", ".join(bd.failedChars),
                   successCount=successCount, successChars=successCharsStr, failureRemain=failureRemain,
                   unresolveCount=unresolveCount))
        gd.setHeadPhoto(data.failurePhotos[failureRemain])     

async def toUserWinState(userMsg: Message, state: FSMContext) -> bool:    
    assert await state.get_state() == "botCharGuess"

    gd = (await state.get_data())["gameData"]
    bd = gd.botData

    if bd.resolvedChars.count("?") == 0:
        # all chars are resolved
        gd.setChatText(text.botUserWin.format(userName=gd.userName, resolvedWord=(" ".join(bd.resolvedChars))))
        gd.setChatMarkup(buidUserReplayKeyboad())

        await drawBotGameState(state)
        await gd.redrawAll(userMsg)
        await state.set_state("botUserWin")

        return True
    else:
        return False
    
async def toBotWinState(userMsg: Message, state: FSMContext) -> bool:    
    assert await state.get_state() == "botCharGuess"

    gd = (await state.get_data())["gameData"]
    bd = gd.botData

    if len(bd.failedChars) >= data.failureNumber:
        # too many failures - user has won
        
        gd.setChatText(text.botBotWin.format(userName=gd.userName, 
                                             guessedChar=bd.guessedChar,
                                             guessedWord=(" ".join(bd.guessedWord)), 
                                             failureNumber=(data.failureNumber-1)))
        gd.setChatMarkup(buidUserReplayKeyboad())
       
        await drawBotGameState(state)
        await gd.redrawAll(userMsg)

        await state.set_state("botBotWin")
        return True
    else:
        return False
    
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
        bd.wordLen = None

    gd.setChatMarkup(None)

    await gd.redrawAll(callback.message)

    redrawMoment:float = 0.0
    async def showProgress(percent: int) -> None:
        nonlocal redrawMoment
        gd.setChatText(text.botRandomWord.format(wordLen=bd.wordLen, percent=percent))
        moment:float = time.time()
        if moment - redrawMoment > 0.5: # provide intervals to suppress weird Telegram errors
            await gd.redrawAll(callback.message)
            redrawMoment = moment 
            await asyncio.sleep(0)     # prevent blocking the task 

    bd.guessedWord   = await findRandomComplexWord(bd.wordLen, showProgress)

    bd.wordLen = len(bd.guessedWord)

    bd.resolvedChars = ["?"] * bd.wordLen
    bd.successChars  = []
    bd.failedChars   = []
    bd.untestedChars = list(char.allChars)
    
    logger.put(text.logBotGuessWord.format(guessedWord=bd.guessedWord))

    gd.setChatText(text.botGuessStart.format(wordLen=bd.wordLen))

    gd.setChatMarkup(buildBoutUntestedKeyboard(bd.untestedChars))

    await drawBotGameState(state)
    await gd.redrawAll(callback.message)

    await state.set_state("botCharGuess")

@router.callback_query(StateFilter("botCharGuess"), F.data.startswith("char_"))
async def bot_open_char(callback: types.CallbackQuery, state: FSMContext):
    gd = (await state.get_data())["gameData"]
    bd = gd.botData

    charPos = int(callback.data.split("_")[1])
    bd.guessedChar = bd.untestedChars.pop(charPos)

    charCount = bd.guessedWord.count(bd.guessedChar)
    if charCount == 0:
        bd.failedChars += bd.guessedChar
        
        if await toBotWinState(callback.message, state):
            return
        
        gd.setChatText(text.botGuessFail.format(userName=gd.userName, guessedChar=bd.guessedChar))
    else:    
        bd.successChars += bd.guessedChar
        for i in [j for j in range(bd.wordLen) if bd.guessedWord[j] == bd.guessedChar]:
            bd.resolvedChars[i] = bd.guessedChar

        if await toUserWinState(callback.message, state):
            return
        
        gd.setChatText(text.botGuessSuccess.format(
            userName=gd.userName, guessedChar=bd.guessedChar, charCount=charCount))

    gd.setChatMarkup(buildBoutUntestedKeyboard(bd.untestedChars))

    await drawBotGameState(state)
    await gd.redrawAll(callback.message)




