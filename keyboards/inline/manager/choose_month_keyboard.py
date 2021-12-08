from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.manager.manager_callbackdatas import choose_worker_for_answers_id, navigate_back_callback, \
    choose_month_callback, choose_test_callback


def get_month(i: int):
    months = {1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель",
              5: "Май", 6: "Июнь", 7: "Июль", 8: "Август",
              9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"}
    return months[i]


def calculate_points(a, b, c, d, e):
    return (a+b+c+d+e)/5


def create_choose_worker_keyboard(workers: list):
    keyboard = InlineKeyboardMarkup()
    for worker in workers:
        keyboard.add(InlineKeyboardButton(text=f"{worker[1]} {worker[2]}",
                                          callback_data=choose_worker_for_answers_id
                                          .new(action="show_answers", user_id=str(worker[0]))))
    keyboard.add(InlineKeyboardButton(text="Отменить", callback_data=navigate_back_callback.new(action="cancel")))
    return keyboard


def create_choose_month_keyboard(answers):
    tests = list()
    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 2
    for item in answers:
        print(item)
        if item[9] not in tests:
            tests.append(item[9])
            keyboard.row(InlineKeyboardButton(text=f"{get_month(item[9])} {item[10]}г.",
                                              callback_data=choose_month_callback.new(action="chosen_m", month=item[9],
                                                                                      year=item[10], user_id=item[1])))
            print(f"{get_month(item[9])} {item[10]}г.")
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data=navigate_back_callback.new(action="back")))
    keyboard.add(InlineKeyboardButton(text="Отменить", callback_data=navigate_back_callback.new(action="cancel")))
    return keyboard


def create_choose_test_keyboard(answers):
    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 2
    for item in answers:
        native_date = item[8]
        date = f"{native_date[-2:]}.{native_date[-5:-3]}.{native_date[0:4]}"
        avr = calculate_points(item[2], item[3], item[4], item[5], item[7])
        text = f"{date} - {str(avr)} баллов"
        keyboard.row(InlineKeyboardButton(text=text, callback_data=choose_test_callback
                                          .new(action="show_test", answers_id=item[0])))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data=navigate_back_callback.new(action="back")))
    keyboard.add(InlineKeyboardButton(text="Отменить", callback_data=navigate_back_callback.new(action="cancel")))
    return keyboard


def create_navigation_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Вернуться к опросам данного сотрудника",
                                      callback_data=navigate_back_callback.new(action="back")))
    keyboard.add(InlineKeyboardButton(text="Вернуться к списку сотрудников",
                                      callback_data=navigate_back_callback.new(action="back2")))
    keyboard.add(InlineKeyboardButton(text="Вернуться в общее меню",
                                      callback_data=navigate_back_callback.new(action="cancel")))
    return keyboard
