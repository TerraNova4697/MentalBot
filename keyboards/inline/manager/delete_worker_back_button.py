from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.manager.manager_callbackdatas import cancel_name_input

back_button = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Отмена", callback_data=cancel_name_input.new(action="c_name_input"))
    ]
])
