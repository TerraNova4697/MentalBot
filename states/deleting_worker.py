from aiogram.dispatcher.filters.state import StatesGroup, State


class DeletingWorker(StatesGroup):
    InputName = State()
    ChooseWorker = State()
