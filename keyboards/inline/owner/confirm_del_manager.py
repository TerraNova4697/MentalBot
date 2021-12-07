from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.owner.owner_callbackdatas import confirm_manager_deleting_callback, \
    cancel_manager_deleting_callback


def create_keyboard(user_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Подтвердить", callback_data=confirm_manager_deleting_callback
                                 .new(action="confirm", user_id=user_id))
        ],
        [
            InlineKeyboardButton(text="Отменить", callback_data=cancel_manager_deleting_callback
                                 .new(action="cancel"))
        ]
    ])
    return keyboard
