from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

manager_main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Посмотреть ответы опросников")
        ],
        [
            KeyboardButton(text="Посмотреть статистику за месяц")
        ],
        [
            KeyboardButton(text="Удалить неактивных сотрудников")
        ]
    ]
)
