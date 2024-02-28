from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram import types

def buildKeyboard(keyRows: list[list[str]]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for kr in keyRows:
        rowButs = []
        for ki in kr:
            rowButs.append(types.InlineKeyboardButton(text=ki[0], callback_data=ki[1]))
        builder.row(*rowButs)      
    return builder.as_markup()              


def buidUserReplayKeyboad():
    return buildKeyboard([
                            [["Да, с радостью", "replay"], ["Нет, надоело", "noreplay"]]
                         ])
