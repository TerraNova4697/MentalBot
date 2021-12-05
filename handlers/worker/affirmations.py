from aiogram import types

from loader import dp, bot
from data.variables import affirmations
from random import randint


@dp.message_handler(text="Аффирмации")
async def send_affirmation(message: types.Message):
    i = randint(0, len(affirmations)-1)
    await bot.send_photo(chat_id=message.chat.id, photo=affirmations[i])
