from gameinfo import GameData
from wordset import WordSet
from common import buidUserReplayKeyboad, buildKeyboard

import data
import text
import logger


from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

def buildUserWordLenKeyboad(wordLen: int):
    return buildKeyboard(
        [
            ([["меньше чем " + str(wordLen), "word_len_dec"]] if wordLen > data.wordLenMin else []) 
              + [[str(wordLen) + " букв(ы)", "word_len_match"]] 
              + ([["больше чем " + str(wordLen), "word_len_inc"]] 
                    if wordLen < data.wordsByLen.size - 1 else []),
            map(lambda i: ["?", "char_" + str(i)], range(wordLen))
        ]
    )


async def chooseWordLen(userMsg: Message, gd: GameData):
    ud = gd.userData

    gd.setChatText(text.userWord.format(userName=gd.userName))
    gd.setChatMarkup(buildUserWordLenKeyboad(ud.wordLen))
    await gd.redrawAll(userMsg)

async def drawUserGameState(state: FSMContext) -> None:
    gd = (await state.get_data())["gameData"]
    ud = gd.userData
    if ud.resolvedChars == None:
        # current game state is empty
        gd.setHeadText("")
    else:
        successCount=len(ud.resolvedChars) - ud.resolvedChars.count("?")
        successCharsStr = ""

        for sc in ud.successChars:
            if successCharsStr != "":
                successCharsStr += ", "
            successCharsStr += sc
            scCount = ud.resolvedChars.count(sc)    
            assert scCount >= 1
            if scCount > 1:
                successCharsStr += f"({scCount})"

        failureRemain = data.failureNumber-len(ud.failedChars)

        gd.setHeadText(text.userGameState.format(resolvedChars=(" ".join(ud.resolvedChars)), wordLen=ud.wordLen,
                   failedCount=len(ud.failedChars), failedChars=", ".join(ud.failedChars),
                   successCount=successCount, successChars=successCharsStr, failureRemain=failureRemain))
        gd.setHeadPhoto(data.failurePhotos[failureRemain])                   

def buildUserGuessCharKeyboad(resolvedChars: list[str], guessedChar: str, firstTry: bool = True):
    return buildKeyboard(
        [
            map(lambda ch_ind: [ch_ind[0], "char_" + str(ch_ind[1])], 
                zip(resolvedChars, range(len(resolvedChars)))),

            [[("Нет буквы " if firstTry else "Больше нет букв ") + guessedChar + " в моем слове", "nochar"]]
        ]
    )

async def toBotWinState(userMsg: Message, state: FSMContext) -> bool:    
    assert await state.get_state() == "userCharGuess"

    gd = (await state.get_data())["gameData"]
    ud = gd.userData

    if ud.resolvedChars.count("?") == 0:
        # all chars are resolved
        
        gd.setChatText(text.userBotWin.format(userName=gd.userName, resolvedWord=(" ".join(ud.resolvedChars)), 
                                              failureRemain=(data.failureNumber-len(ud.failedChars))))
        gd.setChatMarkup(buidUserReplayKeyboad())
       
        await drawUserGameState(state)
        await gd.redrawAll(userMsg)

        logger.put(text.logUserBotWin.format(userName=gd.userName, resolvedWord=("".join(ud.resolvedChars))))

        await state.set_state("userBotWin")

        return True
    else:
        return False

async def toUserWinState(userMsg: Message, state: FSMContext) -> bool:    
    assert await state.get_state() == "userCharGuess"

    gd = (await state.get_data())["gameData"]
    ud = gd.userData

    if len(ud.failedChars) >= data.failureNumber:
        # too many failures - user has won
        
        gd.setChatText(text.userWin.format(userName=gd.userName, unknownWord=(" ".join(ud.resolvedChars)), 
                                           failureNumber=(data.failureNumber-1)))
        gd.setChatMarkup(buidUserReplayKeyboad())
       
        await drawUserGameState(state)
        await gd.redrawAll(userMsg)

        await state.set_state("userWin")

        logger.put(text.logUserWin.format(userName=gd.userName, unknownWord=("".join(ud.resolvedChars))))

        return True
    else:
        return False

async def toUserUnknownWordState(userMsg: Message, state: FSMContext) -> bool:    
    assert await state.get_state() == "userCharGuess"

    gd = (await state.get_data())["gameData"]
    ud = gd.userData

    if ud.candidates.getSize() == 0:
        # Unknown word is detected
        
        gd.setChatText(text.userUnknownWord.format(userName=gd.userName, unknownWord=(" ".join(ud.resolvedChars))))
        gd.setChatMarkup(buidUserReplayKeyboad())

        await drawUserGameState(state)
        gd.setHeadPhoto(data.failurePhotos[0])
        await gd.redrawAll(userMsg)

        logger.put(text.logUserUnknownWord.format(userName=gd.userName, unknownWord=("".join(ud.resolvedChars))))

        await state.set_state("userUnknownWord")
        return True
    else:
        return False

@router.callback_query(StateFilter("userStart", "userBotWin", "userUnknownWord", "userWin", "choiseActor"),  
                       F.data.in_(["user_word", "replay", "user_actor"]))
async def user_word(callback: types.CallbackQuery, state: FSMContext):
    gd = (await state.get_data())["gameData"]
    ud = gd.userData
    ud.wordLen = data.startUserWordLen

    ud.resolvedChars = None # Don't draw userGameState 
    await drawUserGameState(state)
    gd.setHeadText("")
    gd.setHeadPhoto("splash.jpg")

    await chooseWordLen(callback.message, gd)

    await state.set_state("userWordLen")

@router.callback_query(StateFilter("userWordLen"),  F.data.in_(["word_len_dec", "word_len_inc"]))
async def user_word_len_change(callback: types.CallbackQuery, state: FSMContext):
    gd = (await state.get_data())["gameData"]
    ud = gd.userData
    if callback.data == "word_len_dec":
        ud.wordLen -= 1
    else:
        assert callback.data == "word_len_inc"
        ud.wordLen += 1
    await chooseWordLen(callback.message, gd)

@router.callback_query(StateFilter("userWordLen"),  F.data == "word_len_match")
async def user_word_len_match(callback: types.CallbackQuery, state: FSMContext):
    gd = (await state.get_data())["gameData"]
    ud = gd.userData

    ud.resolvedChars = ["?"] * ud.wordLen
    ud.successChars  = []
    ud.failedChars   = []

    ud.candidates = WordSet(ud.wordLen)

    ud.guessedChar = ud.candidates.countMaxChar(ud.resolvedChars)

    ud.charCount = 0
    
    keyboardHelp: str = text.userKeyboardHelp.format(guessedChar=ud.guessedChar) 
    gd.setChatText(text.userGuessStart.format(wordLen=ud.wordLen, guessedChar=ud.guessedChar, keyboardHelp=keyboardHelp))
    gd.setChatMarkup(buildUserGuessCharKeyboad(ud.resolvedChars, 
                                              guessedChar=ud.guessedChar, 
                                              firstTry=True))
    await drawUserGameState(state)
    await gd.redrawAll(callback.message)

    logger.put(text.logUserGuessStart.format(wordLen=ud.wordLen, userName=gd.userName))

    await state.set_state("userCharGuess")

@router.callback_query(StateFilter("userCharGuess"),  F.data == "nochar")
async def user_no_char(callback: types.CallbackQuery, state: FSMContext):
    gd = (await state.get_data())["gameData"]
    ud = gd.userData

    prevChar = ud.guessedChar

    if ud.charCount == 0:
        ud.failedChars.append(ud.guessedChar)

        if await toUserWinState(callback.message, state):
            return

        ud.candidates.filter(absentChar=ud.guessedChar)

        if await toUserUnknownWordState(callback.message, state):
            return

        ud.guessedChar = ud.candidates.countMaxChar(ud.resolvedChars)

        keyboardHelp: str = text.userKeyboardHelp.format(guessedChar=ud.guessedChar) 
        gd.setChatText(text.userGuessFail.format(prevChar=prevChar, guessedChar=ud.guessedChar, keyboardHelp=keyboardHelp))
        gd.setChatMarkup(buildUserGuessCharKeyboad(ud.resolvedChars, 
                                                  guessedChar=ud.guessedChar, 
                                                  firstTry=True))
        await drawUserGameState(state)
        await gd.redrawAll(callback.message)
    else:
        if await toBotWinState(callback.message, state):
            return
        
        ud.candidates.filter(existChar=ud.guessedChar, resolvedChars=ud.resolvedChars)

        if await toUserUnknownWordState(callback.message, state):
            return
    
        ud.guessedChar = ud.candidates.countMaxChar(ud.resolvedChars)

        ud.charCount = 0
        
        keyboardHelp: str = text.userKeyboardHelp.format(guessedChar=ud.guessedChar) 
        gd.setChatText(text.userGuessSuccess.format(prevChar=prevChar, guessedChar=ud.guessedChar, keyboardHelp=keyboardHelp))
        gd.setChatMarkup(buildUserGuessCharKeyboad(ud.resolvedChars, guessedChar=ud.guessedChar, 
                                                                    firstTry=(ud.charCount == 0)))
        await drawUserGameState(state)
        await gd.redrawAll(callback.message) 

    print(f"\n***** Candidates ({ud.candidates.getSize()}):")
    if ud.candidates.getSize() > 150:
        print("too many")
    else:        
        print(ud.candidates.getWords())                                                                       

@router.callback_query(StateFilter("userCharGuess"), F.data.startswith("char_"))
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

    match ud.charCount:
        case 0:
            ud.successChars.pop()
        case 1:
            if curChar == '?':
                ud.successChars.append(ud.guessedChar)

    gd.setChatMarkup(buildUserGuessCharKeyboad(ud.resolvedChars, guessedChar=ud.guessedChar, 
                                                                    firstTry=(ud.charCount == 0)))
    await drawUserGameState(state)
    await gd.redrawAll(callback.message)                                                                    
