from aiogram.dispatcher.filters.state import StatesGroup, State


class ShowAnswers(StatesGroup):
    NameInput = State()
    ChooseWorker = State()
    ChooseMonth = State()
    Answers = State()
    Final = State()