from aiogram import types

from loader import dp, bot
from data.variables import music
from random import randint


@dp.message_handler(text="Музыка")
async def send_music(message: types.Message):
    i = randint(0, len(music)-1)
    await bot.send_message(chat_id=message.chat.id, text=music[i])
