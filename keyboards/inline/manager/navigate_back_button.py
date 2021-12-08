from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.manager.manager_callbackdatas import navigate_back_callback

navigate_back_button = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Отменить", callback_data=navigate_back_callback.new(action="back"))
    ]
])
