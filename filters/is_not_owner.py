from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.variables import owner


class IsNotOwner(BoundFilter):

    async def check(self, message: types.Message) -> bool:
        print(str(message.chat.id) not in owner)
        return str(message.chat.id) not in owner
