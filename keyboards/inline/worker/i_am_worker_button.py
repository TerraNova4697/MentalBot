from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Клавиатура, появляющаяся при нажатии /start. Можно выбрать ветку диалога с ботом
from keyboards.inline.worker.worker_callback_data import i_am_worker_button_callback

i_am_worker_button = InlineKeyboardMarkup(row_width=1,
                                          inline_keyboard=[
                                              [
                                                  InlineKeyboardButton(text="Я сотрудник",
                                                                       callback_data=i_am_worker_button_callback
                                                                       .new(action="to_worker_branch"))
                                              ],
                                              [
                                                  InlineKeyboardButton(text="Я менеджер",
                                                                       callback_data=i_am_worker_button_callback
                                                                       .new(action="to_manage_branch"))
                                              ]
                                          ])
