from aiogram import Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

import keyboards as kb
import database.services as db
from fsm_states import ChooseAnswerFSM
import messages as ms

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message) -> None:
    """Start message"""
    await message.answer("Бот поможет вам найти ответ на вопрос по интересующей вас теме.\n\n"
                         "Для поиска ответа выберите команду\n/answers во вкладке \"Меню\" или нажмите на команду прямо в сообщении.")


@router.message(Command("answers"))
@router.callback_query(lambda callback: callback.data.split("_")[0] == "back" and callback.data.split("_")[1] == "to-group")
async def start_handler(message: types.Message | types.CallbackQuery, state: FSMContext) -> None:
    """Выбор группы, начало ChooseAnswerFSM"""
    # при возвращении назад
    if type(message) == types.CallbackQuery:
        await state.clear()

    groups = db.get_all_groups()
    await state.set_state(ChooseAnswerFSM.group)

    # при возвращении назад
    if type(message) == types.CallbackQuery:
        await message.message.edit_text("Выберите группу...", reply_markup=kb.select_group_keyboard(groups).as_markup())

    # при прямом выборе
    else:
        await message.answer("Выберите группу...", reply_markup=kb.select_group_keyboard(groups).as_markup())


@router.callback_query(ChooseAnswerFSM.group, lambda callback: callback.data != "cancel")
@router.callback_query(lambda callback: callback.data.split("_")[0] == "back" and callback.data.split("_")[1] == "to-subgroup")
async def choose_subgroup_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Выбор подгруппы, запись группы в FSM storage"""
    # при возвращении назад
    if "_" in callback.data:
        data = await state.get_data()
        group_id = data["group_id"]
    # при прямом выборе
    else:
        group_id = int(callback.data)

    await state.update_data(group_id=group_id)

    subgroups = db.get_all_subgroups_by_group_id(group_id=group_id)

    await state.set_state(ChooseAnswerFSM.subgroup)
    await callback.message.edit_text("Выберите подгруппу...",
                                     reply_markup=kb.select_subgroup_keyboard(subgroups).as_markup())


@router.callback_query(ChooseAnswerFSM.subgroup, lambda callback: callback.data != "cancel")
async def choose_question_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Выбор вопроса, запись подгруппы в FSM storage"""
    subgroup_id = int(callback.data)
    await state.update_data(subgroup_id=subgroup_id)

    questions = db.get_all_questions_by_subgroup_id(subgroup_id=subgroup_id)

    await state.set_state(ChooseAnswerFSM.question)
    message = ms.get_questions(questions)
    await callback.message.edit_text(message, reply_markup=kb.select_question_keyboard(questions).as_markup())


@router.callback_query(ChooseAnswerFSM.question, lambda callback: callback.data != "cancel")
async def answer_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Ответ на вопрос, окончание ChooseAnswerFSM"""
    question_id = int(callback.data)
    await state.update_data(question_id=question_id)

    data = await state.get_data()
    await state.clear()

    answers = db.get_all_answers_by_question_id(question_id=data["question_id"])
    for a in answers:
        await callback.message.answer(a.text)

    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass


@router.callback_query(lambda callback: callback.data == "cancel", StateFilter("*"))
async def cancel_handler(callback: types.CallbackQuery, state: FSMContext):
    """Cancel FSM and delete last message"""
    await state.clear()
    await callback.message.answer("Действие отменено ❌")
    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass

