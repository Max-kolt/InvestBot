from aiogram import Router, F, Bot
from aiogram.types import Message
from loguru import logger
from config import ADMIN
from utils import send_to_user


admin_router = Router(name='Admin')
admin_router.message.filter(F.chat.id == ADMIN)


@admin_router.message()
async def admin(message: Message, bot: Bot):
    if not message.reply_to_message:
        return
    if message.reply_to_message.from_user.username == (name := await bot.me()).username:
        user_id = message.reply_to_message.text.split(' ')[0][1::]
        await send_to_user(bot=bot, user_id=user_id, text=message.text)
        await message.answer(text=f"Ответ по id {user_id} отправлен")
        logger.info(f"Sending feedback to {user_id}")
