from aiogram.dispatcher.filters.state import StatesGroup, State


class ConfirmEmail(StatesGroup):
    InputEmail = State()