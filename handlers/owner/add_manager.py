from aiogram import types
from aiogram.types import CallbackQuery

from filters import IsOwner, IsOwnerCall
from keyboards.default.manager_main_keyboard import manager_main_menu_keyboard
from keyboards.inline.owner.owner_callbackdatas import confirm_new_manager_callback
from loader import dp, bot, db

text = "Сообщите менеджеру скрытую команду /admin, которую нужно ввести в бот, для активации возможностей менеджера. " \
       "Вам придет уведомление о подтверждении с данными аккаунта менеджера. Подтвердите или отклоните."

notify_admin_added = "Приветствую менеджера! Вы можете выбрать следующие функции:"


@dp.message_handler(IsOwner(), text="Добавить менеджера")
async def add_manager(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=text)


@dp.callback_query_handler(confirm_new_manager_callback.filter(action="confirm"), IsOwnerCall())
async def confirm_manager(call: CallbackQuery, callback_data: dict):
    print(call.message.text)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    manager_id = callback_data.get("user_id")
    manager = db.select_manager_by_user_id(user_id=int(manager_id))
    print(manager)
    db.update_manager(user_id=int(manager_id), status="Active")
    await bot.send_message(chat_id=call.message.chat.id,
                           text=f"Пользователь {manager[0]} {manager[1]} {manager[2]}"
                           f" принят в качестве менеджера и имеет доступ к статистике")
    await bot.send_message(chat_id=manager_id, text=notify_admin_added, reply_markup=manager_main_menu_keyboard)


