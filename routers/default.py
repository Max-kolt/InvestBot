from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton,\
    ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
import asyncio
from loguru import logger

from utils import main_keyboard, start_keyboard
from states import RegistrationForm
from database import Investor

default_router = Router(name="Default")


@default_router.message(CommandStart())
async def welcome(message: Message, state: FSMContext):
    utm_metka = message.text.split(" ")[-1] if message.text != "/start" else "other"

    await message.answer_photo(
        photo=FSInputFile("static/Icon.jpg"),
        caption=
        "Приветствую Вас! Я помощник Atlant Capital, с удовольствием помогу масштабировать Ваш бизнес, "
        "а так же дам самую ценную информацию, чтобы Вы точно смогли привлечь инвестиции в свой проект. ",
        reply_markup=start_keyboard
    )

    if not Investor.select().where(Investor.login == message.from_user.username):
        Investor.create(login=message.from_user.username, chat_id=message.from_user.id, utm_metka=utm_metka)


    # else:
    #     (Investor.update({'available': True}).where(Investor.chat_id == message.from_user.id)).execute()
    #     await message.answer("Вы уже прошли начальную регистрацию.\nХотите зарегистрироваться заново?",
    #                          reply_markup=ReplyKeyboardMarkup(keyboard=[
    #                              [KeyboardButton(text='Заново зарегистрироваться')],
    #                              [KeyboardButton(text="Отменить")]
    #                          ], resize_keyboard=True))
    #     return
    #
    # logger.info(f"User {message.from_user.username} start registration")
    # await message.answer("""Как вас зовут?""")
    # await state.set_state(RegistrationForm.name)


@default_router.message(Command('main_menu'))
async def main_menu(message: Message):
    await message.answer(text="Главное меню", reply_markup=main_keyboard)

