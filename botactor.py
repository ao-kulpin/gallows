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

@router.callback_query(StateFilter("choiseActor"),  
                       F.data.in_(["bot_actor"]))
async def bot_word(callback: types.CallbackQuery, state: FSMContext):
