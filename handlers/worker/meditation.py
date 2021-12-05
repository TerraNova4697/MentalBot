from aiogram import types

from loader import dp, bot
from random import randint
from data.variables import meditation


@dp.message_handler(text="Медитации")
async def send_meditation(message: types.Message):
    i = randint(0, len(meditation)-1)
    await bot.send_message(chat_id=message.chat.id, text=meditation[i])
