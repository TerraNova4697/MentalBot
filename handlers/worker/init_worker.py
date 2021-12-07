from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data import variables
from keyboards.default.workers_main_keyboard import workers_main_keyboard
from keyboards.inline.worker.worker_callback_data import i_am_worker_button_callback
from loader import dp, bot, db

# Получаем апдейт от сотрудника. Проверяем есть ли он в базе. Если положительно, то:
from states.register_worker import RegisterWorker


# Получаем апдейт от сотрудника. Проверяем есть ли он в базе. Если отрицательно, то регистрируем:
@dp.callback_query_handler(i_am_worker_button_callback.filter(action="to_worker_branch"))
async def init_worker(call: CallbackQuery):
    await call.answer()
    await bot.send_message(chat_id=call.message.chat.id, text="Введите Вашу фамилию")
    await RegisterWorker.InputName.set()


@dp.message_handler(state=RegisterWorker.InputName)
async def workers_name(message: types.Message, state: FSMContext):
    await state.update_data(
        {
            "name": message.text
        }
    )
    await bot.send_message(chat_id=message.chat.id, text="Введите Имя")
    await RegisterWorker.InputSurname.set()


@dp.message_handler(state=RegisterWorker.InputSurname)
async def workers_name(message: types.Message, state: FSMContext):
    await state.update_data(
        {
            "surname": message.text
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
    await state.finish()
    variables.workers.append(int(message.chat.id))
    db.add_worker(message.chat.id, name=name, surname=surname, patronym=patronym)
    await bot.send_message(chat_id=message.chat.id, text="Вы можете выбрать следующее:",
                           reply_markup=workers_main_keyboard)

