from typing import Callable, Dict, Any, Awaitable, List

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from database.services import get_all_admins


class CheckIsAdminMiddleware(BaseMiddleware):
    """Проверка является ли пользователь админом"""
    def __init__(self, env_admins: List[str]):
        self.admins = env_admins

    def is_admin(self, tg_id) -> bool:
        if str(tg_id) not in [admin.tg_id for admin in get_all_admins()] + self.admins:
            return False
        return True

    async def __call__(self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]) -> Any:

        # проверяем является ли пользователь админом
        if self.is_admin(data["event_from_user"].id):
            return await handler(event, data)

        # ответ для обычных пользователей
        await event.answer(
            "Эта функция доступна только администраторам",
            show_alert=True
        )
        return


class CheckPrivateMessageMiddleware(BaseMiddleware):
    """Проверка сообщения в лс, а не группу"""
    async def __call__(self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]) -> Any:

        # проверяем является ли пользователь админом
        if data["event_chat"].type == "private":
            return await handler(event, data)
        return


