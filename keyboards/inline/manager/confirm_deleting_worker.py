from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.manager.manager_callbackdatas import confirm_deleting_worker_callback


def create_keyboard(user_id):
    confirm_deleting_worker = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Удалить", callback_data=confirm_deleting_worker_callback
                                 .new(action="delete", user_id=user_id))
        ],
        [
            InlineKeyboardButton(text="Отменить", callback_data=confirm_deleting_worker_callback
                                 .new(action="cancel", user_id=user_id))
        ]
    ])
    return confirm_deleting_worker
