from aiogram.fsm.state import StatesGroup, State


class CreateAnswerFSM(StatesGroup):
    group = State()
    subgroup = State()
    question = State()


class ChooseAnswerFSM(StatesGroup):
    group = State()
    subgroup = State()
    question = State()


