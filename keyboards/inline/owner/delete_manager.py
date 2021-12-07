from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.owner.owner_callbackdatas import choose_manager_callback, choose_manager_cancel_callback
from loader import db


def create_delete_manager_keyboard():
    managers_list = db.select_all_managers(status="Active")
    keyboard = InlineKeyboardMarkup()
    for manager in managers_list:
        keyboard.add(InlineKeyboardButton(text=f"{manager[1]} {manager[2]}", callback_data=choose_manager_callback
                                          .new(action="delete", user_id=manager[0])))
    keyboard.add(InlineKeyboardButton(text="Отменить", callback_data=choose_manager_cancel_callback
                                      .new(action="cancel")))
    return keyboard
