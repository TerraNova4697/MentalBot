from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.worker.worker_callback_data import q1_callback, q2_callback, q3_callback, q4_callback, q6_callback

q1 = InlineKeyboardMarkup(row_width=5, inline_keyboard=[
    [
        InlineKeyboardButton(text="1", callback_data=q1_callback.new(question="one", answer='1'))
    ],
    [
        InlineKeyboardButton(text="2", callback_data=q1_callback.new(question="one", answer='2'))
    ],
    [
        InlineKeyboardButton(text="3", callback_data=q1_callback.new(question="one", answer='3'))
    ],
    [
        InlineKeyboardButton(text="4", callback_data=q1_callback.new(question="one", answer='4'))
    ],
    [
        InlineKeyboardButton(text="5", callback_data=q1_callback.new(question="one", answer='5'))
    ]
])

q2 = InlineKeyboardMarkup(row_width=5, inline_keyboard=[
    [
        InlineKeyboardButton(text="1", callback_data=q2_callback.new(question="two", answer='1'))
    ],
    [
        InlineKeyboardButton(text="2", callback_data=q2_callback.new(question="two", answer='2'))
    ],
    [
        InlineKeyboardButton(text="3", callback_data=q2_callback.new(question="two", answer='3'))
    ],
    [
        InlineKeyboardButton(text="4", callback_data=q2_callback.new(question="two", answer='4'))
    ],
    [
        InlineKeyboardButton(text="5", callback_data=q2_callback.new(question="two", answer='5'))
    ]
])

q3 = InlineKeyboardMarkup(row_width=5, inline_keyboard=[
    [
        InlineKeyboardButton(text="1", callback_data=q3_callback.new(question="three", answer='1'))
    ],
    [
        InlineKeyboardButton(text="2", callback_data=q3_callback.new(question="three", answer='2'))
    ],
    [
        InlineKeyboardButton(text="3", callback_data=q3_callback.new(question="three", answer='3'))
    ],
    [
        InlineKeyboardButton(text="4", callback_data=q3_callback.new(question="three", answer='4'))
    ],
    [
        InlineKeyboardButton(text="5", callback_data=q3_callback.new(question="three", answer='5'))
    ]
])

q4 = InlineKeyboardMarkup(row_width=5, inline_keyboard=[
    [
        InlineKeyboardButton(text="1", callback_data=q4_callback.new(question="four", answer='1'))
    ],
    [
        InlineKeyboardButton(text="2", callback_data=q4_callback.new(question="four", answer='2'))
    ],
    [
        InlineKeyboardButton(text="3", callback_data=q4_callback.new(question="four", answer='3'))
    ],
    [
        InlineKeyboardButton(text="4", callback_data=q4_callback.new(question="four", answer='4'))
    ],
    [
        InlineKeyboardButton(text="5", callback_data=q4_callback.new(question="four", answer='5'))
    ]
])

q6 = InlineKeyboardMarkup(row_width=5, inline_keyboard=[
    [
        InlineKeyboardButton(text="1", callback_data=q6_callback.new(question="six", answer='1'))
    ],
    [
        InlineKeyboardButton(text="2", callback_data=q6_callback.new(question="six", answer='2'))
    ],
    [
        InlineKeyboardButton(text="3", callback_data=q6_callback.new(question="six", answer='3'))
    ],
    [
        InlineKeyboardButton(text="4", callback_data=q6_callback.new(question="six", answer='4'))
    ],
    [
        InlineKeyboardButton(text="5", callback_data=q6_callback.new(question="six", answer='5'))
    ]
])
