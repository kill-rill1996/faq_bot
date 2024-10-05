from aiogram import Bot
from config import GROUP_ID


async def send_notification(bot: Bot):
    """Уведомление о боте в группу"""
    msg = " ❗<i>Напоминание:</i>\n\n" \
          "Для поиска ответов на вопросы вы можете воспользоваться нашим телеграм ботом @FAQQQTestBot\n\n" \
          "<b>Важно:</b> бот отвечает только в личных сообщениях"

    await bot.send_message(GROUP_ID, msg)