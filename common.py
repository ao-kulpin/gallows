from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

def buidUserReplayKeyboad():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="Да, с радостью", callback_data="replay"),       
        types.InlineKeyboardButton(text="Нет, надоело", callback_data="noreplay")        
    )
    return builder.as_markup()
