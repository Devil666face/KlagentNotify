from database import Database
from aiogram import types
from aiogram.types import ReplyKeyboardRemove,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.types.message import ContentTypes
from aiogram.types.message import ContentType

class Keyboards:
    def inline_add_user_buttons(self, to_add_user_id, to_add_user_name):
        inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
        true_button = types.InlineKeyboardButton(text='Да', callback_data=f'useradd_1_{to_add_user_id}_{to_add_user_name}')
        false_button = types.InlineKeyboardButton(text='Нет', callback_data=f'useradd_0_{to_add_user_id}_{to_add_user_name}')
        inline_keyboard.row(true_button,false_button)
        return inline_keyboard