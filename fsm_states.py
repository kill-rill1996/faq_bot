from aiogram.fsm.state import StatesGroup, State


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


class CreateAnswerFSM(StatesGroup):
    choose_group = State()
    choose_subgroup = State()
    choose_answer = State()
    text = State()


class CreateAdminFSM(StatesGroup):
    contact = State()


class DeleteAdminFSM(StatesGroup):
    admin_id = State()
    confirm = State()


class DeleteAnswerFSM(StatesGroup):
    group = State()
    subgroup = State()
    question = State()
    answer = State()
    confirm = State()
