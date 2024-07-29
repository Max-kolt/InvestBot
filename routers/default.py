from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton,\
    ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
import asyncio
from loguru import logger

from utils import main_keyboard
from states import RegistrationForm
from database import Investor

default_router = Router(name="Default")


@default_router.message(CommandStart())
async def welcome(message: Message, state: FSMContext):
    await message.answer_photo(
        photo=FSInputFile("static/Icon.jpg"),
        caption=
        "Приветствую вас! Я помощник Atlant Capital. Я с удовольствием помогу Вам масштабировать бизнес, "
        "а так же дам самую необходимую информацию, чтобы Вы точно смогли привлечь инвестиции в свой проект.\n\n"
        "Давайте сперва познакомимся поближе, а после я пришлю Вам топ-12 ошибок, "
        "исправив которые ваши шансы привлечь инвестиции вырастут на 70%",
        reply_markup=ReplyKeyboardRemove()
    )
    await asyncio.sleep(2)

    if not Investor.select().where(Investor.login == message.from_user.username):
        Investor.create(login=message.from_user.username, chat_id=message.from_user.id)
    else:
        await message.answer("Вы уже прошли начальную регистрацию.\nХотите зарегистрироваться заново?",
                             reply_markup=ReplyKeyboardMarkup(keyboard=[
                                 [KeyboardButton(text='Заново зарегистрироваться')],
                                 [KeyboardButton(text="Отмена")]
                             ], resize_keyboard=True))
        return

    logger.info(f"User {message.from_user.username} start registration")
    await message.answer("""Как вас зовут?""")
    await state.set_state(RegistrationForm.name)


# @default_router.message(Command('main_menu'))
# async def main_menu(message: Message):
#     await message.answer(text="Главное меню", reply_markup=main_keyboard)

