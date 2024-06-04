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

def wordLenSuffix(worrdLen: int):
    return str(worrdLen) + ("х" if worrdLen < 5 else "ти")
