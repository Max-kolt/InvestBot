from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.fsm.context import FSMContext
from loguru import logger

from states import SendPostForm
from config import ADMIN
from utils import send_to_user
from database import Investor


admin_router = Router(name='Admin')
admin_router.message.filter(F.chat.id == ADMIN)


@admin_router.message(Command("send_all_users"))
async def admin_send_all(message: Message, state: FSMContext):
    await state.set_state(SendPostForm.post)
    await message.answer("Запишсь пошла.\nОтправьте в следующем сообщении то, что необходимо отправить всем "
                         "пользователям телеграмм бота.")


@admin_router.message(SendPostForm.post)
async def admin_process_send_all(message: Message, state: FSMContext):
    users = Investor.select()
    logger.info("Start posting to all bot users")
    for user in users:
        try:
            await message.copy_to(user.chat_id)
        except TelegramForbiddenError:
            logger.exception(f"Can't send post to {user.chat_id}")
        except Exception as e:
            logger.exception(f"Can't send post to {user.chat_id}: {e}")
    logger.info("Finishing posting to all bot users")
    await state.clear()
    await message.answer('Рассылка прошла успешно')


@admin_router.message()
async def admin_feedback(message: Message, bot: Bot):
    if not message.reply_to_message:
        return
    if message.reply_to_message.from_user.username == (name := await bot.me()).username:
        if message.reply_to_message.text:
            user_id = message.reply_to_message.text.split(' ')[0][1::]
        elif message.reply_to_message.caption:
            user_id = message.reply_to_message.caption.split(' ')[0][1::]
        else:
            logger.exception(f"Can't filter message with id: {message.message_id}")
            return
        try:
            await send_to_user(bot=bot, user_id=user_id, text=message.text)
            await message.answer(text=f"Ответ по id {user_id} отправлен")
            logger.info(f"Sending feedback to {user_id}")
        except TelegramForbiddenError:
            await message.answer(text="Пользователь больше не доступен")
            logger.error(f"User with id {user_id} not available")
            (Investor.update({'available': False}).where(Investor.chat_id == user_id)).execute()

