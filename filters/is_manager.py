from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery

from data.variables import managers


class IsManager(BoundFilter):

    async def check(self, message: types.Message) -> bool:
        print()
        return message.chat.id in managers


class IsManagerCall(BoundFilter):

    async def check(self, call: CallbackQuery) -> bool:
        return call.message.chat.id in managers
