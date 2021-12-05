from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data import variables
from keyboards.inline.worker.worker_callback_data import i_am_worker_button_callback
from loader import dp, bot


# Получаем апдейт от сотрудника. Проверяем есть ли он в базе. Если положительно, то:
from states.register_worker import RegisterWorker


# Получаем апдейт от сотрудника. Проверяем есть ли он в базе. Если отрицательно, то регистрируем:
@dp.callback_query_handler(i_am_worker_button_callback.filter(action="to_worker_branch"))
async def init_worker(call: CallbackQuery):
    await bot.send_message(chat_id=call.message.chat.id, text="Введите Ваше имя")
    await RegisterWorker.InputSurname.set()


@dp.message_handler(state=RegisterWorker.InputSurname)
async def workers_name(message: types.Message, state: FSMContext):
    await state.update_data(
        {
            "surname": message.text
        }
    )
    await bot.send_message(chat_id=message.chat.id, text="Введите Фамилию")
    await RegisterWorker.InputName.set()


@dp.message_handler(state=RegisterWorker.InputName)
async def workers_name(message: types.Message, state: FSMContext):
    await state.update_data(
        {
            "name": message.text
        }
    )
    await bot.send_message(chat_id=message.chat.id, text="Введите Отчество")
    await RegisterWorker.InputPatronym.set()


@dp.message_handler(state=RegisterWorker.InputPatronym)
async def workers_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    surname = data.get("surname")
    name = data.get("name")
    patronym = message.text
    await bot.send_message(chat_id=message.chat.id, text=f"{surname} {name} {patronym}")
    await state.finish()
    variables.workers.append(message.chat.id)

