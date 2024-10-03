import aiogram
from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter

from config import ADMINS
from middleware import CheckIsAdminMiddleware
from database.services import get_all_groups, get_all_subgroups_by_group_id, get_all_questions_by_subgroup_id, get_all_answers_by_question_id

router = Router()
router.message.middleware.register(CheckIsAdminMiddleware(ADMINS))


@router.message(Command("add_answer"))
async def echo(message: types.Message) -> None:
    """Добавление ответа на вопрос"""
    await message.answer(message.text)

