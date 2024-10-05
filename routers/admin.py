from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from config import ADMINS
from middleware import CheckIsAdminMiddleware
from fsm_states import CreateGroupFSM, CreateSubGroupFSM, CreateQuestionFSM, CreateAnswerFSM, CreateAdminFSM
import keyboards as kb
import routers.utils as utils
import database.services as db
import messages as ms

router = Router()
admin_middleware = CheckIsAdminMiddleware(ADMINS)
router.message.middleware.register(admin_middleware)
# router.message.middleware.register(CheckIsAdminMiddleware(ADMINS))


@router.message(Command("add_admin"))
async def add_admin(message: types.Message, state: FSMContext) -> None:
    """Добавление админа, начало FSM"""
    await state.set_state(CreateAdminFSM.contact)
    msg = await message.answer("Отправьте контакт нового администратора через вкладку 'Прикрепить'",
                         reply_markup=kb.cancel_keyboard().as_markup())
    await state.update_data(prev_mess=msg)


@router.message(F.contact, CreateAdminFSM.contact)
async def save_admin(message: types.Message, state: FSMContext) -> None:
    """Сохранение админа, окончание FSM"""
    contact = message.contact
    tg_id = str(contact.user_id)

    # если админ уже есть
    if utils.is_admin_exists(tg_id):
        data = await state.get_data()
        try:
            await data["prev_mess"].delete()
        except TelegramBadRequest:
            pass
        msg = await message.answer("Пользователь уже является администратором, отправьте другой контакт",
                                   reply_markup=kb.cancel_keyboard().as_markup())
        await state.update_data(prev_mess=msg)
        return

    # новый админ
    else:
        db.create_admin(tg_id=tg_id)
        admin_middleware.admins += tg_id

        data = await state.get_data()
        try:
            await data["prev_mess"].delete()
        except TelegramBadRequest:
            pass
        await state.clear()

        await message.answer("Новый администратор успешно добавлен!")


# BLOCK OTHER TYPES
@router.message(~F.content_type.in_({'text', 'contact'}), StateFilter("*"))
async def block_types_handler(message: types.Message) -> None:
    await message.answer("Некорректный тип данных в сообщении (принимается только текст)")


# ADD GROUP
@router.message(Command("add_group"))
async def create_group(message: types.Message, state: FSMContext) -> None:
    """Начало создание группы, начало CreateGroupFSM"""
    await state.set_state(CreateGroupFSM.title)

    msg = await message.answer("Отправьте название новой группы",
                               reply_markup=kb.cancel_keyboard().as_markup())
    await state.update_data(prev_mess=msg)


@router.message(CreateGroupFSM.title, F.content_type.in_({'text'}))
async def save_group(message: types.Message, state: FSMContext) -> None:
    group_title = message.text

    if utils.is_group_already_created(group_title):
        await message.answer(f"Группа с названием <b>{group_title}</b> уже существует!",
                             reply_markup=kb.cancel_keyboard().as_markup())
    else:
        db.create_group(group_title)
        data = await state.get_data()
        try:
            await data["prev_mess"].delete()
        except TelegramBadRequest:
            pass
        await state.clear()
        await message.answer(f"Группа <b>{group_title}</b> создана! ✅")


# ADD SUBGROUP
@router.message(Command("add_subgroup"))
async def create_subgroup(message: types.Message, state: FSMContext) -> None:
    """Начало создание группы, начало CreateSubGroupFSM"""
    await state.set_state(CreateSubGroupFSM.choose_group)

    all_groups = db.get_all_groups()

    msg = await message.answer("Выберите группу, в которую хотите добавить:",
                               reply_markup=kb.create_group_keyboard(all_groups).as_markup())

    await state.update_data(prev_mess=msg)


@router.callback_query(CreateSubGroupFSM.choose_group)
async def choose_group(callback: types.CallbackQuery, state: FSMContext) -> None:
    group_id = int(callback.data)
    await state.update_data(group_id=group_id)

    await state.set_state(CreateSubGroupFSM.title)
    msg = await callback.message.edit_text("Отправьте название новой подгруппы",
                               reply_markup=kb.cancel_keyboard().as_markup())

    await state.update_data(prev_mess=msg)


@router.message(CreateSubGroupFSM.title, F.content_type.in_({'text'}))
async def save_subgroup(message: types.Message, state: FSMContext) -> None:
    subgroup_title = message.text
    data = await state.get_data()

    if utils.is_subgroup_already_created(subgroup_title, data["group_id"]):
        try:
            await data["prev_mess"].delete()
        except TelegramBadRequest:
            pass
        msg = await message.answer(f"Подгруппа с названием <b>{subgroup_title}</b> уже существует!",
                             reply_markup=kb.cancel_keyboard().as_markup())
        await state.update_data(prev_mess=msg)
    else:
        db.create_subgroup(subgroup_title, data["group_id"])

        try:
            await data["prev_mess"].delete()
        except TelegramBadRequest:
            pass

        await state.clear()
        await message.answer(f"Подгруппа <b>{subgroup_title}</b> создана! ✅")


# ADD QUESTION
@router.message(Command("add_question"))
async def create_question(message: types.Message, state: FSMContext) -> None:
    await state.set_state(CreateQuestionFSM.choose_group)

    all_groups = db.get_all_groups()

    msg = await message.answer("Выберите группу, в которую хотите добавить:",
                               reply_markup=kb.create_group_keyboard(all_groups).as_markup())

    await state.update_data(prev_mess=msg)


@router.callback_query(CreateQuestionFSM.choose_group)
async def choose_group_q(callback: types.CallbackQuery, state: FSMContext) -> None:
    group_id = int(callback.data)
    await state.update_data(group_id=group_id)

    await state.set_state(CreateQuestionFSM.choose_subgroup)

    all_groups = db.get_all_subgroups_by_group_id(group_id)
    await callback.message.edit_text("Выберите подгруппу, в которую хотите добавить:",
                               reply_markup=kb.create_subgroup_keyboard(all_groups).as_markup())


@router.callback_query(CreateQuestionFSM.choose_subgroup)
async def choose_subgroup_q(callback: types.CallbackQuery, state: FSMContext) -> None:
    subgroup_id = int(callback.data)
    await state.update_data(subgroup_id=subgroup_id)

    await state.set_state(CreateQuestionFSM.title)
    await callback.message.edit_text("Отправьте новый вопрос",
                               reply_markup=kb.cancel_keyboard().as_markup())


@router.message(CreateQuestionFSM.title, F.content_type.in_({'text'}))
async def save_subgroup(message: types.Message, state: FSMContext) -> None:
    question_title = message.text
    data = await state.get_data()

    if utils.is_question_already_created(question_title, data["subgroup_id"]):
        try:
            await data["prev_mess"].delete()
        except TelegramBadRequest:
            pass

        msg = await message.answer(f"Такой вопрос <b>{question_title}</b> уже существует! Введите другой вопрос",
                             reply_markup=kb.cancel_keyboard().as_markup())
        await state.update_data(prev_mess=msg)
    else:
        db.create_question(question_title, data["subgroup_id"])

        try:
            await data["prev_mess"].delete()
        except TelegramBadRequest:
            pass

        await state.clear()
        await message.answer(f'Вопрос <b>"{question_title}"</b> создан! ✅')


# ADD ANSWER
@router.message(Command("add_answer"))
async def create_answer(message: types.Message, state: FSMContext) -> None:
    await state.set_state(CreateAnswerFSM.choose_group)

    all_groups = db.get_all_groups()

    msg = await message.answer("Выберите группу, в которую хотите добавить:",
                               reply_markup=kb.create_group_keyboard(all_groups).as_markup())

    await state.update_data(prev_mess=msg)


@router.callback_query(CreateAnswerFSM.choose_group)
async def choose_group_a(callback: types.CallbackQuery, state: FSMContext) -> None:
    group_id = int(callback.data)
    await state.update_data(group_id=group_id)

    await state.set_state(CreateAnswerFSM.choose_subgroup)

    all_groups = db.get_all_subgroups_by_group_id(group_id)
    await callback.message.edit_text("Выберите подгруппу, в которую хотите добавить:",
                               reply_markup=kb.create_subgroup_keyboard(all_groups).as_markup())


@router.callback_query(CreateAnswerFSM.choose_subgroup)
async def choose_subgroup_a(callback: types.CallbackQuery, state: FSMContext) -> None:
    subgroup_id = int(callback.data)
    await state.update_data(subgroup_id=subgroup_id)
    await state.set_state(CreateAnswerFSM.choose_answer)

    all_questions = db.get_all_questions_by_subgroup_id(subgroup_id)
    questions_text = ms.get_questions_text(all_questions)

    await callback.message.edit_text(questions_text, reply_markup=kb.create_question_keyboard(all_questions).as_markup())


@router.callback_query(CreateAnswerFSM.choose_answer)
async def choose_subgroup_q(callback: types.CallbackQuery, state: FSMContext) -> None:
    question_id = int(callback.data)
    await state.update_data(question_id=question_id)

    await state.set_state(CreateAnswerFSM.text)
    await callback.message.edit_text("Отправьте новый ответ на вопрос", reply_markup=kb.cancel_keyboard().as_markup())


@router.message(CreateAnswerFSM.text, F.content_type.in_({'text'}))
async def save_answer(message: types.Message, state: FSMContext) -> None:
    answer_text = message.text
    data = await state.get_data()

    db.create_answer(answer_text, data["question_id"])

    try:
        await data["prev_mess"].delete()
    except TelegramBadRequest:
        pass

    await state.clear()
    await message.answer(f'Ответ создан! ✅')


@router.callback_query(lambda callback: callback.data == "cancel", StateFilter("*"))
async def cancel_handler(callback: types.CallbackQuery, state: FSMContext):
    """Cancel FSM and delete last message"""
    await state.clear()
    await callback.message.answer("Действие отменено ❌")
    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass
