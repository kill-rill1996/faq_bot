from aiogram.fsm.state import StatesGroup, State


class CreateAnswerFSM(StatesGroup):
    group = State()
    subgroup = State()
    question = State()
    answer = State()


class ChooseAnswerFSM(StatesGroup):
    group = State()
    subgroup = State()
    question = State()


class CreateGroupFSM(StatesGroup):
    title = State()


class CreateSubGroupFSM(StatesGroup):
    choose_group = State()
    title = State()


class CreateQuestionFSM(StatesGroup):
    choose_group = State()
    choose_subgroup = State()
    title = State()
