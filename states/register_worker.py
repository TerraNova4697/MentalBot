from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterWorker(StatesGroup):
    InputSurname = State()
    InputName = State()
    InputPatronym = State()
