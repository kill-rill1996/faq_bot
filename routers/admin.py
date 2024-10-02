import aiogram
from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter

from config import ADMINS
from middleware import CheckIsAdminMiddleware

router = Router()
router.message.middleware.register(CheckIsAdminMiddleware(ADMINS))


@router.message(Command("add_answer"))
async def echo(message: types.Message) -> None:
    """"""
    await message.answer(f"{message.from_user.id}\n")
    await message.answer(f"{message.message_id}\n")


