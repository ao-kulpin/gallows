from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram import types

def buildKeyboard(keyRows: list[list[list[str]]]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for kr in keyRows:
        builder.row(
            *map(lambda kdef: types.InlineKeyboardButton(text=kdef[0], callback_data=kdef[1]), kr)
        )
    return builder.as_markup()              

def buidUserReplayKeyboad():
    return buildKeyboard(
        [
            [["Да, с радостью", "replay"], ["Нет, надоело", "noreplay"]]
        ])

def wordLenSuffix(wordLen: int):
    return str(wordLen) + \
        ("-х"    if wordLen < 5 \
                else \
                
        ("-и"   if wordLen > 6 and wordLen < 9 
                else \
        "ти"))
