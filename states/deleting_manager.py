from aiogram.dispatcher.filters.state import StatesGroup, State


class DeletingManager(StatesGroup):
    ChooseManager = State()
    ConfirmDeleting = State()
