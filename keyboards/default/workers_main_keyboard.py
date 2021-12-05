from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

workers_main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Аффирмации")
    ],
    [
        KeyboardButton(text="Музыка")
    ],
    [
        KeyboardButton(text="Медитации")
    ],
    [
        KeyboardButton(text="Пройти опрос")
    ],
],
    resize_keyboard=True)
