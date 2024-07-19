from aiogram.methods import SendMessage, SendDocument
from config import ADMIN
from aiogram import Bot


async def send_to_admin(bot: Bot, text: str = None, document: str = None, message_effect: str = None):
    if document:
        await bot(SendDocument(chat_id=ADMIN, document=document, caption=text, message_effect_id=message_effect))
    else:
        await bot(SendMessage(chat_id=ADMIN, text=text, message_effect_id=message_effect))


async def send_to_user(bot: Bot, user_id: str, text: str):
    await bot(SendMessage(chat_id=user_id, text=text))
