from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

owner_main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Посмотреть ответы опросников")
        ],
        [
            KeyboardButton(text="Посмотреть статистику за месяц")
        ],
        [
            KeyboardButton(text="Добавить менеджера")
        ],
        [
            KeyboardButton(text="Удалить менеджера")
        ],
        [
            KeyboardButton(text="Удалить неактивных сотрудников")
        ]
    ]
)
