from aiogram import types
from aiogram.dispatcher.filters import Command

from filters import IsOwner
from keyboards.default.owner_main_keyboard import owner_main_menu_keyboard
from loader import dp, bot

main_menu_text = "Приветствую владельца!\n\nВы можете выбрать следующие функции:"


@dp.message_handler(Command('owner'), IsOwner())
async def init_owner(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=main_menu_text, reply_markup=owner_main_menu_keyboard)
