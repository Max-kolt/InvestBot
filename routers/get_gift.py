from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.exceptions import TelegramNotFound
from loguru import logger

from config import CHANNEL_NAME, CHANNEL_LINK

gift_router = Router(name='Gift')


# @gift_router.message(F.text == "Получить подарок")
# async def get_gift(message: Message):
#     await message.answer(text="В подарок за подписку тебя ждёт чек-лист, который поможет "
#                               "тебе на 70% быстрее привлечь инвестиции. \n\n" + CHANNEL_LINK,
#                          reply_markup=InlineKeyboardMarkup(inline_keyboard=[
#                              [InlineKeyboardButton(text="Забрать подарок", callback_data='get_gift')]
#                          ]))


@gift_router.callback_query(F.data == 'get_gift')
async def process_gift(call: CallbackQuery, bot: Bot):
    try:
        await bot.get_chat_member("@"+CHANNEL_NAME, call.from_user.id)
    except TelegramNotFound as n:
        await call.message.answer("Вас не обнаружили в списке подписчиков канала, "
                                  "проверьте вашу подписку и попробуйте еще раз.")
        logger.exception(n.message)
        return
    except Exception as e:
        await call.message.answer('Ошибка сервера, уведомление отправлено администратору.\nПовторите попытку позже.')
        logger.exception(e)
        return

    await call.message.answer_document(document=FSInputFile('static/check-list.pdf'), caption="Держите ваш подарок 🎁")
