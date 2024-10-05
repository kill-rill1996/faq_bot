import asyncio
import aiogram as io
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault

from config import BOT_TOKEN
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
        BotCommand(command="add_admin", description="Добавить администратора"),
        BotCommand(command="help", description="Инструкция и поддержка"),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def set_description(bot: io.Bot):
    """Описание бота до запуска"""
    await bot.set_my_description("Бот поможет найти ответы на вопросы по бухгалтерии\n\nДля запуска бота нажмите /start")


async def start_bot() -> None:
    """Запуск бота"""
    bot = io.Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await set_commands(bot)
    await set_description(bot)

    storage = MemoryStorage()
    dispatcher = io.Dispatcher(storage=storage)

    # scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    # scheduler.add_job(apsched.send_balance_report, trigger="cron", year='*', month='*', day="*", hour=21,
    #                   minute=0, second=0, start_date=datetime.now(), kwargs={"bot": bot})
    # scheduler.start()

    dispatcher.include_routers(admin.router, users.router)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    print("Запуск бота...")
    database.create_db()
    asyncio.run(start_bot())
