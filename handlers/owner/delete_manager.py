from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from filters import IsOwner, IsOwnerCall
from keyboards.inline.owner.confirm_del_manager import create_keyboard
from keyboards.inline.owner.delete_manager import create_delete_manager_keyboard
from keyboards.inline.owner.owner_callbackdatas import choose_manager_cancel_callback, choose_manager_callback, \
    cancel_manager_deleting_callback, confirm_manager_deleting_callback
from loader import dp, bot, db
from states.deleting_manager import DeletingManager
from data.variables import managers


@dp.message_handler(IsOwner(), text="Удалить менеджера")
async def deleting_manager(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Выберите менеджера",
                           reply_markup=create_delete_manager_keyboard())
    await DeletingManager.ChooseManager.set()


@dp.callback_query_handler(choose_manager_cancel_callback.filter(action="cancel"), IsOwnerCall(),
                           state=DeletingManager.ChooseManager)
async def cancel_choosing(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(choose_manager_callback.filter(action="delete"), IsOwnerCall(),
                           state=DeletingManager.ChooseManager)
async def confirm_deleting(call: CallbackQuery, callback_data: dict):
    manager_id = callback_data.get("user_id")
    manager = db.select_manager_by_user_id(user_id=int(manager_id))
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"Подтвердите удаление менеджера {manager[0]} {manager[1]}",
                                reply_markup=create_keyboard(user_id=manager_id))
    await DeletingManager.ConfirmDeleting.set()


@dp.callback_query_handler(cancel_manager_deleting_callback.filter(action="cancel"), IsOwnerCall(),
                           state=DeletingManager.ConfirmDeleting)
async def cancel_deleting(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(confirm_manager_deleting_callback.filter(action="confirm"), IsOwnerCall(),
                           state=DeletingManager.ConfirmDeleting)
async def delete_manager(call: CallbackQuery, callback_data: dict, state: FSMContext):
    manager_id = callback_data.get("user_id")
    manager = db.select_manager_by_user_id(user_id=int(manager_id))
    db.inactivate_manager(user_id=int(manager_id))
    managers.remove(int(manager_id))
    await bot.edit_message_text(text=f"Вы успешно удалили менеджера {manager[0]} {manager[1]}. "
                                     "Больше он не сможет посмотреть ответы или статистику по сотрудникам.",
                                chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()
