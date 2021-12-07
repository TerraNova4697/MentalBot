from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from filters import IsManager, IsOwner, IsOwnerCall, IsManagerCall
from keyboards.inline.manager.confirm_deleting_worker import create_keyboard
from keyboards.inline.manager.delete_worker_back_button import back_button
from keyboards.inline.manager.manager_callbackdatas import cancel_name_input, delete_worker_callback, \
    cancel_button_choose_worker_to_delete, confirm_deleting_worker_callback
from loader import dp, bot, db
from states.deleting_worker import DeletingWorker
from data.variables import workers


def create_keyboard_of_workers(list_of_workers):
    keyboard = InlineKeyboardMarkup()
    for worker in list_of_workers:
        keyboard.add(InlineKeyboardButton(text=f"{worker[1]} {worker[2]}", callback_data=delete_worker_callback
                                          .new(action="delete", user_id=worker[0])))
    keyboard.add(InlineKeyboardButton(text="Отмена", callback_data=cancel_button_choose_worker_to_delete
                                      .new(action="cancel")))
    return keyboard


@dp.message_handler(IsManager(), text="Удалить неактивных сотрудников")
@dp.message_handler(IsOwner(), text="Удалить неактивных сотрудников")
async def input_name(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Введите фамилию сотрудника", reply_markup=back_button)
    await DeletingWorker.InputName.set()


@dp.callback_query_handler(cancel_name_input.filter(action="c_name_input"),
                           IsManagerCall(), state=DeletingWorker.InputName)
@dp.callback_query_handler(cancel_name_input.filter(action="c_name_input"),
                           IsOwnerCall(), state=DeletingWorker.InputName)
async def cancel_input(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.message_handler(IsManager(), state=DeletingWorker.InputName)
@dp.message_handler(IsOwner(), state=DeletingWorker.InputName)
async def find_worker(message: types.Message):
    await DeletingWorker.ChooseWorker.set()
    list_of_workers = db.select_all_workers_by_name(name=message.text, status="Active")
    keyboard = create_keyboard_of_workers(list_of_workers)
    await bot.send_message(chat_id=message.chat.id, text="Выберите сотрудника", reply_markup=keyboard)


@dp.callback_query_handler(cancel_button_choose_worker_to_delete.filter(action="cancel"),
                           IsManagerCall(), state=DeletingWorker.ChooseWorker)
@dp.callback_query_handler(cancel_button_choose_worker_to_delete.filter(action="cancel"),
                           IsOwnerCall(), state=DeletingWorker.ChooseWorker)
async def cancel_input(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(delete_worker_callback.filter(action="delete"), IsManagerCall(),
                           state=DeletingWorker.ChooseWorker)
@dp.callback_query_handler(delete_worker_callback.filter(action="delete"), IsOwnerCall(),
                           state=DeletingWorker.ChooseWorker)
async def confirm_deleting(call: CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = callback_data.get("user_id")
    worker = db.select_worker_by_id(user_id=user_id)
    text = f"Подтвердите удаление сотрудника {worker[0][1]} {worker[0][2]} " \
           f"(запрещаете доступ к боту для этого сотрудника)"
    keyboard = create_keyboard(worker[0][0])
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                text=text,
                                reply_markup=keyboard,
                                message_id=call.message.message_id)


@dp.callback_query_handler(confirm_deleting_worker_callback.filter(action="cancel"),
                           IsManagerCall(), state=DeletingWorker.ChooseWorker)
@dp.callback_query_handler(confirm_deleting_worker_callback.filter(action="cancel"),
                           IsOwnerCall(), state=DeletingWorker.ChooseWorker)
async def cancel_deleting(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(confirm_deleting_worker_callback.filter(action="delete"),
                           IsManagerCall(), state=DeletingWorker.ChooseWorker)
@dp.callback_query_handler(confirm_deleting_worker_callback.filter(action="delete"),
                           IsOwnerCall(), state=DeletingWorker.ChooseWorker)
async def delete_worker(call: CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = callback_data.get("user_id")
    db.inactivate_worker(user_id=user_id)
    worker = db.select_worker_by_id(user_id=user_id)
    workers.remove(int(user_id))
    await bot.edit_message_text(text=f"Вы успешно удалили сотрудника {worker[0][1]} {worker[0][2]}. "
                                     "Больше он не будет учитываться в статистике и его ответы не будут фиксироваться.",
                                chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()

