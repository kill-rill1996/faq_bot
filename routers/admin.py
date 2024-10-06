from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from config import ADMINS
from middleware import CheckIsAdminMiddleware, CheckPrivateMessageMiddleware
from fsm_states import (CreateGroupFSM, CreateSubGroupFSM, CreateQuestionFSM,
                        CreateAnswerFSM, CreateAdminFSM, DeleteAdminFSM, DeleteAnswerFSM)
import keyboards as kb
import routers.utils as utils
import database.services as db
import messages as ms

router = Router()
router.message.middleware.register(CheckPrivateMessageMiddleware())
router.message.middleware.register(CheckIsAdminMiddleware(ADMINS))


# ADD ADMIN
@router.message(Command("add_admin"))
async def add_admin(message: types.Message, state: FSMContext) -> None:
    """Добавление админа, начало FSM"""
    await state.set_state(CreateAdminFSM.contact)
    msg = await message.answer("Отправьте карточку контакта нового администратора через вкладку 'Прикрепить'",
                               reply_markup=kb.cancel_keyboard().as_markup())
    await state.update_data(prev_mess=msg)


@router.message(~F.content_type.in_({'contact'}), CreateAdminFSM.contact)
async def wrong_contact_data(message: types.Message, state: FSMContext) -> None:
    """Если отправлена не карточка контакта"""
    data = await state.get_data()
    try:
        await data["prev_mess"].delete()
    except TelegramBadRequest:
        pass

    msg = await message.answer("Необходимо отправить <b>карточку контакта</b> через вкладку 'Прикрепить'",
                               reply_markup=kb.cancel_keyboard().as_markup())
    await state.update_data(prev_mess=msg)


@router.message(F.contact, CreateAdminFSM.contact)
async def save_admin(message: types.Message, state: FSMContext) -> None:
    """Сохранение админа, окончание FSM"""
    contact = message.contact
    tg_id = str(contact.user_id)
    tg_phone = contact.phone_number

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

    # новый админ
    else:
        db.create_admin(tg_id=tg_id, phone=tg_phone)

        data = await state.get_data()
        try:
            await data["prev_mess"].delete()
        except TelegramBadRequest:
            pass
        await state.clear()

        await message.answer("Новый администратор успешно добавлен ✅")


# DELETE ADMIN
@router.message(Command("delete_admin"))
async def delete_admin(message: types.Message, state: FSMContext) -> None:
    """Удаление администратора из БД"""
    admins_from_db = db.get_all_admins()
    await state.set_state(DeleteAdminFSM.admin_id)
    msg = await message.answer("Выберите номер администратора, которого хотите удалить:",
                         reply_markup=kb.all_admins_keyboard(admins_from_db).as_markup())
    await state.update_data(prev_mess=msg)


@router.callback_query(DeleteAdminFSM.admin_id, lambda callback: callback.data.split("_")[0] == "delete")
async def pick_admin_to_delete(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Выбор админа для удаления"""
    admin_id = int(callback.data.split("_")[1])
    admin = db.get_admin_by_id(admin_id)

    await state.set_state(DeleteAdminFSM.confirm)
    await state.update_data(id=admin_id)

    text = f"Удалить администратора id: <b>{admin.tg_id}</b>"
    if admin.phone:
        text += f" телефон: <b>{admin.phone}</b>"

    text += "?"
    await callback.message.edit_text(text=text, reply_markup=kb.confirm_keyboard().as_markup())


@router.callback_query(DeleteAdminFSM.confirm, lambda callback: callback.data.split("_")[0] == "confirm")
async def confirmation_delete(callback: types.CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()

    if callback.data.split("_")[1] == "yes":
        deleted_admin = db.delete_admin_by_id(data["id"])

        text = f"Администратор с id <b>{deleted_admin.tg_id}</b>"
        if deleted_admin.phone:
            text += f" и телефоном <b>{deleted_admin.phone}</b>"
        text += " удален ✅"

        try:
            await data["prev_mess"].delete()
        except TelegramBadRequest:
            pass

        await state.clear()
        await callback.message.answer(text)
        return

    try:
        await data["prev_mess"].delete()
    except TelegramBadRequest:
        pass
    await state.clear()
    await callback.message.answer("Действие отменено ❌")


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


@router.callback_query(CreateSubGroupFSM.choose_group, lambda callback: callback.data != "cancel")
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


@router.callback_query(CreateQuestionFSM.choose_group, lambda callback: callback.data != "cancel")
async def choose_group_q(callback: types.CallbackQuery, state: FSMContext) -> None:
    group_id = int(callback.data)
    await state.update_data(group_id=group_id)

    await state.set_state(CreateQuestionFSM.choose_subgroup)

    all_groups = db.get_all_subgroups_by_group_id(group_id)
    await callback.message.edit_text("Выберите подгруппу, в которую хотите добавить:",
                               reply_markup=kb.create_subgroup_keyboard(all_groups).as_markup())


@router.callback_query(CreateQuestionFSM.choose_subgroup, lambda callback: callback.data != "cancel")
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


@router.callback_query(CreateAnswerFSM.choose_group, lambda callback: callback.data != "cancel")
async def choose_group_a(callback: types.CallbackQuery, state: FSMContext) -> None:
    group_id = int(callback.data)
    await state.update_data(group_id=group_id)

    await state.set_state(CreateAnswerFSM.choose_subgroup)

    all_groups = db.get_all_subgroups_by_group_id(group_id)
    await callback.message.edit_text("Выберите подгруппу, в которую хотите добавить:",
                               reply_markup=kb.create_subgroup_keyboard(all_groups).as_markup())


@router.callback_query(CreateAnswerFSM.choose_subgroup, lambda callback: callback.data != "cancel")
async def choose_subgroup_a(callback: types.CallbackQuery, state: FSMContext) -> None:
    subgroup_id = int(callback.data)
    await state.update_data(subgroup_id=subgroup_id)
    await state.set_state(CreateAnswerFSM.choose_answer)

    all_questions = db.get_all_questions_by_subgroup_id(subgroup_id)
    questions_text = ms.get_questions_text(all_questions)

    await callback.message.edit_text(questions_text, reply_markup=kb.create_question_keyboard(all_questions).as_markup())


@router.callback_query(CreateAnswerFSM.choose_answer, lambda callback: callback.data != "cancel")
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


# DELETE ANSWER
@router.message(Command("delete_answer"))
@router.callback_query(lambda callback: callback.data.split("_")[0] == "back" and callback.data.split("_")[1] == "to-groups")
async def delete_question(message: types.Message | types.CallbackQuery, state: FSMContext) -> None:
    """Выбор группы, начало DeleteAnswerFSM"""
    # при возвращении назад
    if type(message) == types.CallbackQuery:
        await state.clear()

    groups = db.get_all_groups()

    await state.set_state(DeleteAnswerFSM.group)

    # при возвращении назад
    if type(message) == types.CallbackQuery:
        msg = await message.message.edit_text("Выберите группу...", reply_markup=kb.select_group_to_delete_keyboard(groups).as_markup())

    # при прямом выборе
    else:
        msg = await message.answer("Выберите группу...", reply_markup=kb.select_group_to_delete_keyboard(groups).as_markup())

    await state.update_data(prev_mess=msg)

@router.callback_query(DeleteAnswerFSM.group, lambda callback: callback.data != "cancel")
@router.callback_query(lambda callback: callback.data.split("_")[0] == "back" and callback.data.split("_")[1] == "to-subgroups")
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

    await state.set_state(DeleteAnswerFSM.subgroup)

    # если группа пустая
    if not subgroups:
        await callback.message.edit_text("В данной группе вопросов пока нет",
                                         reply_markup=kb.select_subgroup_to_delete_keyboard(subgroups).as_markup())
        return

    await callback.message.edit_text("Выберите подгруппу...",
                                     reply_markup=kb.select_subgroup_to_delete_keyboard(subgroups).as_markup())


@router.callback_query(DeleteAnswerFSM.subgroup, lambda callback: callback.data != "cancel")
@router.callback_query(lambda callback: callback.data.split("_")[0] == "back" and callback.data.split("_")[1] == "to-questions")
async def choose_question_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Выбор вопроса, запись подгруппы в FSM storage"""
    # при возвращении назад
    if "_" in callback.data:
        data = await state.get_data()
        subgroup_id = data["subgroup_id"]
    # при прямом выборе
    else:
        subgroup_id = int(callback.data)

    await state.update_data(subgroup_id=subgroup_id)

    questions = db.get_all_questions_by_subgroup_id(subgroup_id=subgroup_id)

    await state.set_state(DeleteAnswerFSM.question)

    # если подгруппа пустая
    if not questions:
        await callback.message.edit_text("В данной подгруппе вопросов пока нет",
                                         reply_markup=kb.select_question_to_delete_keyboard(questions).as_markup())
        return

    message = ms.get_questions_to_delete(questions)
    await callback.message.edit_text(message, reply_markup=kb.select_question_to_delete_keyboard(questions).as_markup())


@router.callback_query(DeleteAnswerFSM.question, lambda callback: callback.data != "cancel")
@router.callback_query(lambda callback: callback.data.split("_")[0] == "back" and callback.data.split("_")[1] == "to-answers")
async def choose_answer_to_delete(callback: types.CallbackQuery, state: FSMContext) -> None:
    # при возвращении назад
    if "_" in callback.data:
        data = await state.get_data()
        question_id = data["question_id"]

    # при прямом выборе
    else:
        question_id = int(callback.data)

    question_title = db.get_question_by_id(question_id).title

    answers = db.get_all_answers_by_question_id(question_id)
    if not answers:
        await callback.message.edit_text("В данном вопросе пока нет ответов",
                                         reply_markup=kb.back_to_question_delete_keyboard().as_markup())
        return

    await state.set_state(DeleteAnswerFSM.answer)

    msg = ms.get_answers_to_delete(answers, question_title)
    await callback.message.edit_text(msg, reply_markup=kb.select_answer_to_delete_keyboard(answers).as_markup())


@router.callback_query(DeleteAnswerFSM.answer, lambda callback: callback.data != "cancel")
async def answer_delete_confirm_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Ответ на вопрос, окончание ChooseAnswerFSM"""
    answer_id = int(callback.data)
    await state.update_data(answer_id=answer_id)

    answer = db.get_answer_by_id(answer_id)
    await state.set_state(DeleteAnswerFSM.confirm)


    await callback.message.edit_text(f'Удалить ответ: <b>"{answer.text}"</b>?', reply_markup=kb.confirm_keyboard().as_markup())


@router.callback_query(DeleteAnswerFSM.confirm, lambda callback: callback.data != "cancel")
async def answer_delete_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()

    if callback.data.split("_")[1] == "yes":
        try:
            await data["prev_mess"].delete()
        except TelegramBadRequest:
            pass

        answer = db.delete_answer_by_id(data["answer_id"])
        await callback.message.answer(f"Ответ <b>\"{answer.text}\"</b> удален ✅")

        return

    try:
        await data["prev_mess"].delete()
    except TelegramBadRequest:
        pass

    await callback.message.answer("Удаление отменено ❌")





# CANCEL BUTTON
@router.callback_query(lambda callback: callback.data == "cancel", StateFilter("*"))
async def cancel_handler(callback: types.CallbackQuery, state: FSMContext):
    """Cancel FSM and delete last message"""
    await state.clear()
    await callback.message.answer("Действие отменено ❌")
    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass

