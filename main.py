import asyncio
import aiogram as io
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault

from config import BOT_TOKEN
from database.services import create_fake_data
from routers import admin, users
from database import database


async def set_commands(bot: io.Bot):
    """Перечень команд для бота"""
    commands = [
        BotCommand(command="answers", description="Найти ответ"),
        BotCommand(command="add_group", description="Добавить группу"),
        BotCommand(command="add_subgroup", description="Добавить подгруппу"),
        BotCommand(command="add_question", description="Добавить вопрос"),
        BotCommand(command="add_answer", description="Добавить ответ"),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_bot() -> None:
    """Запуск бота"""
    bot = io.Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await set_commands(bot)

    storage = MemoryStorage()
    dispatcher = io.Dispatcher(storage=storage)

    # scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    # scheduler.add_job(apsched.send_balance_report, trigger="cron", year='*', month='*', day="*", hour=21,
    #                   minute=0, second=0, start_date=datetime.now(), kwargs={"bot": bot})
    # scheduler.start()

    dispatcher.include_routers(users.router, admin.router)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    print("Запуск бота...")
    database.create_db()
    # create_fake_data()
    asyncio.run(start_bot())
