from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data.variables import managers, owner, accessed_emails
from filters import IsOwner, IsManager
from keyboards.inline.manager.manager_callbackdatas import navigate_back_callback, update_email_callback
from keyboards.inline.manager.navigate_back_button import navigate_back_button
from keyboards.inline.manager.update_email import renew_keyboard
from loader import dp, bot, db
from states.confirm_email import ConfirmEmail
from utils.google_sheets import give_access


@dp.message_handler(IsOwner(), text="Посмотреть статистику за месяц")
@dp.message_handler(IsManager(), text="Посмотреть статистику за месяц")
async def send_url(message: types.Message):
    if str(message.chat.id) not in accessed_emails:
        await bot.send_message(chat_id=message.chat.id, text="Пожалуйста, введите Вашу действующую Гугл-почту, "
                                                             "чтобы я смог предоставить Вам доступ к таблице",
                               reply_markup=navigate_back_button)
        await ConfirmEmail.InputEmail.set()
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text="https://docs.google.com/spreadsheets/d/1ED4N7L-iacwPp9s0ymqF4g-VYDlnfsz7SwGJ3R0VZk4/edit#gid=0",
                               reply_markup=renew_keyboard)


@dp.callback_query_handler(navigate_back_callback.filter(action="back"), state=ConfirmEmail.InputEmail)
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(IsOwner(), state=ConfirmEmail.InputEmail)
@dp.message_handler(IsManager(), state=ConfirmEmail.InputEmail)
async def validate_email(message: types.Message, state: FSMContext):
    db.update_managers_email(email=message.text, user_id=int(message.chat.id))
    accessed_emails.append(message.chat.id)
    give_access(message.text)
    await state.finish()
    await bot.send_message(chat_id=message.chat.id,
                           text="https://docs.google.com/spreadsheets/d/1ED4N7L-iacwPp9s0ymqF4g-VYDlnfsz7SwGJ3R0VZk4/edit#gid=0",
                           reply_markup=renew_keyboard)


@dp.callback_query_handler(update_email_callback.filter(action="update"))
async def update_email(call: CallbackQuery):
    await call.answer()
    await bot.send_message(chat_id=call.message.chat.id, text="Пожалуйста, введите Вашу действующую Гугл-почту, "
                                                              "чтобы я смог предоставить Вам доступ к таблице",
                           reply_markup=navigate_back_button)
    await ConfirmEmail.InputEmail.set()
