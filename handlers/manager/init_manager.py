from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from filters import IsNotOwner
from keyboards.inline.owner.confirm_keyboard import create_keyboard_to_confirm
from loader import dp, bot, db
from states.register_manager import RegisterManager
from data.variables import owner

notify_owner_text = "Сотрудник ______(ФИО) отправил запрос на права менеджера."
notified_text = "Мы отправили ваш запрос на права менеджера. Пожалуйста, дождитесь подтверждения."


@dp.message_handler(Command('admin'), IsNotOwner())
async def init_manager(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Введите свою фамилию")
    await RegisterManager.InputName.set()


@dp.message_handler(state=RegisterManager.InputName)
async def request_surname(message: types.Message, state: FSMContext):
    await state.update_data({"name": message.text})
    await bot.send_message(chat_id=message.chat.id, text="Введите свое имя")
    await RegisterManager.InputSurname.set()


@dp.message_handler(state=RegisterManager.InputSurname)
async def request_patronym(message: types.Message, state: FSMContext):
    await state.update_data({"surname": message.text})
    await bot.send_message(chat_id=message.chat.id, text="Введите свое отчество")
    await RegisterManager.InputPatronym.set()


@dp.message_handler(state=RegisterManager.InputPatronym)
async def notify_owner(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    surname = data.get("surname")
    patronym = message.text
    print(message.chat.id)
    db.add_manager(user_id=message.chat.id, name=name, surname=surname, patronym=patronym)
    await bot.send_message(chat_id=owner[0],
                           text=f"Сотрудник {name} {surname} {patronym} отправил запрос на права менеджера.",
                           reply_markup=create_keyboard_to_confirm(user_id=message.chat.id))
    await bot.send_message(chat_id=message.chat.id, text=notified_text)
    await state.finish()
