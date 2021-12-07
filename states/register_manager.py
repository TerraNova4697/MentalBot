from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterManager(StatesGroup):
    InputName = State()
    InputSurname = State()
    InputPatronym = State()
