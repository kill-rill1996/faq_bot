import aiogram
from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from config import ADMINS
from middleware import CheckIsAdminMiddleware
from fsm_states import CreateAnswerFSM
import keyboards as kb
import database.services as db
import messages as ms

router = Router()
router.message.middleware.register(CheckIsAdminMiddleware(ADMINS))


@router.message(Command("add_answer"))
async def create_group(message: types.Message, state: FSMContext) -> None:
    """Выбор группы, начало CreateAnswerFSM"""
    await state.set_state(CreateAnswerFSM.group)

    groups = db.get_all_groups()

    msg = await message.answer("Выберите группу или отправьте название группы текстом, чтобы создать новую",
                               reply_markup=kb.create_group_keyboard(groups).as_markup())

    await state.update_data(prev_mess=msg)


@router.callback_query(CreateAnswerFSM.group)
@router.message(CreateAnswerFSM.group)
async def create_subgroup(message: types.CallbackQuery | types.Message, state: FSMContext) -> None:
    """Выбор подгруппы, запись группы FSM storage"""
    # имеющаяся группа
    if type(message) == types.CallbackQuery:
        group_id = int(message.data)
        await state.update_data(group_id=group_id)

        await state.set_state(CreateAnswerFSM.subgroup)

        subgroups = db.get_all_subgroups_by_group_id(group_id)

        await message.message.edit_text(
            "Выберите подгруппу или отправьте название подгруппы текстом, чтобы создать новую",
            reply_markup=kb.create_subgroup_keyboard(subgroups).as_markup()
        )

    # новая группа
    else:
        group_title = message.text


        # group_id = db.create_group(message.text)

        await state.update_data(group_title=group_title)
        # await state.update_data(group_id=group_id)

        await state.set_state(CreateAnswerFSM.subgroup)

        try:
            data = await state.get_data()
            await data["prev_mess"].delete()
        except TelegramBadRequest:
            pass

        msg = await message.answer("Введите название подгруппы", reply_markup=kb.cancel_keyboard().as_markup())
        await state.update_data(prev_mess=msg)


@router.callback_query(CreateAnswerFSM.subgroup)
@router.message(CreateAnswerFSM.subgroup)
async def create_question(message: types.CallbackQuery | types.Message, state: FSMContext) -> None:
    """Выбор вопроса, запись подгруппы FSM storage"""
    # имеющаяся подгруппа
    if type(message) == types.CallbackQuery:
        subgroup_id = int(message.data)
        await state.update_data(subgroup_id=subgroup_id)

        await state.set_state(CreateAnswerFSM.question)

        questions = db.get_all_questions_by_subgroup_id(subgroup_id)
        mess = ms.get_questions(questions, creation=True)

        await message.message.edit_text(mess, reply_markup=kb.create_question_keyboard(questions).as_markup())

    # новая подгруппа
    else:
        data = await state.get_data()
        group_id = data["group_id"]
        subgroup_id = db.create_subgroup(message.text, group_id)
        await state.update_data(subgroup_id=subgroup_id)

        await state.set_state(CreateAnswerFSM.question)

        try:
            data = await state.get_data()
            await data["prev_mess"].delete()
        except TelegramBadRequest:
            pass

        msg = await message.answer("Отправьте вопрос текстом", reply_markup=kb.cancel_keyboard().as_markup())
        await state.update_data(prev_mess=msg)


@router.callback_query(CreateAnswerFSM.question)
@router.message(CreateAnswerFSM.question)
async def create_answer(message: types.CallbackQuery | types.Message, state: FSMContext) -> None:
    """Создание ответа, вопроса FSM storage"""
    # имеющийся вопрос
    if type(message) == types.CallbackQuery:
        question_id = int(message.data)
        await state.update_data(question_id=question_id)

        await state.set_state(CreateAnswerFSM.answer)
        await message.message.edit_text("Введите ответ", reply_markup=kb.cancel_keyboard().as_markup())

    # новый вопрос
    else:
        data = await state.get_data()
        subgroup_id = data["subgroup_id"]
        question_id = db.create_question(message.text, subgroup_id)
        await state.update_data(question_id=question_id)

        await state.set_state(CreateAnswerFSM.answer)

        try:
            data = await state.get_data()
            await data["prev_mess"].delete()
        except TelegramBadRequest:
            pass

        msg = await message.answer("Введите ответ", reply_markup=kb.cancel_keyboard().as_markup())
        await state.update_data(prev_mess=msg)


@router.message(CreateAnswerFSM.answer)
async def create_answer_finish(message: types.Message, state: FSMContext) -> None:
    """Запись вопроса в бд, окончание CreateAnswerFSM"""
    answer_text = message.text
    data = await state.get_data()
    question_id = data["question_id"]
    db.create_answer(answer_text, question_id)

    await data["prev_mess"].delete()
    await state.clear()

    await message.answer("Вопрос успешно создан")


@router.callback_query(lambda callback: callback.data == "cancel", StateFilter("*"))
async def cancel_handler(callback: types.CallbackQuery, state: FSMContext):
    """Cancel FSM and delete last message"""
    await state.clear()
    await callback.message.answer("Действие отменено ❌")
    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass
