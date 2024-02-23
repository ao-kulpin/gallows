from gameinfo import GameData

import data
import text

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

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


async def chooseWordLen(userMsg: Message, gd: GameData):
    ud = gd.userData

    gd.setChatText(text.userWord.format(userName=gd.userName))
    gd.setChatMarkup(buidUserWordLenKeyboad(ud.wordLen))
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

        gd.setHeadText(text.userGameState.format(resolvedChars=(" ".join(ud.resolvedChars)), wordLen=ud.wordLen,
                   failedCount=len(ud.failedChars), failedChars=", ".join(ud.failedChars),
                   successCount=successCount, successChars=successCharsStr, failureRemain=(data.failureNumber-len(ud.failedChars))))

async def chooseWordLen(userMsg: Message, gd: GameData):
    ud = gd.userData

    gd.setChatText(text.userWord.format(userName=gd.userName))
    gd.setChatMarkup(buidUserWordLenKeyboad(ud.wordLen))
    await gd.redrawAll(userMsg)

@router.callback_query(StateFilter("userStart", "userBotWin", "userUnknownWord", "userWin"),  F.data.in_(["user_word", "replay"]))
async def user_word(callback: types.CallbackQuery, state: FSMContext):
    gd = (await state.get_data())["gameData"]
    ud = gd.userData
    ud.wordLen = data.startUserWordLen

    ud.resolvedChars = None # Don't draw userGameState 
    await drawUserGameState(state)

    await chooseWordLen(callback.message, gd)

    await state.set_state("userWordLen")
