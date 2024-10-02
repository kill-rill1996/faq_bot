from aiogram.fsm.state import StatesGroup, State


class CreateAnswerFSM(StatesGroup):
    group = State()
    sub_group = State()
    question = State()


