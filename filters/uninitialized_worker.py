from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery

from data import variables


class IsWorkerInitialized(BoundFilter):
    async def check(self, call: CallbackQuery) -> bool:
        if call.message.chat.id in variables.workers:
            return True
        else:
            return False
