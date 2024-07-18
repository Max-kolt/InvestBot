from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
import asyncio
from loguru import logger
from states import RegistrationForm
from database import Investor

default_router = Router(name="Default")


@default_router.message(CommandStart())
async def welcome(message: Message, state: FSMContext):
    await message.answer_photo(
        photo=FSInputFile("static/Icon.jpg"),
        caption=
        "Приветствую вас! Я помощник Atlant Capital. "
        "Я с удовольствием помогу вам приблизить свой бизнес к масштабированию, "
        "а так же дам самую необходимую вам информацию, "
        "чтобы вы точно смогли привлечь инвестиции в свой проект. "
        "Давайте сперва познакомимся поближе?"
    )
    await asyncio.sleep(4)

    # if not Investor.select().where(Investor.login == message.from_user.username):
    #     Investor.create(login=message.from_user.username, chat_id=message.from_user.id)

    logger.info(f"User {message.from_user.username} start registration")
    await message.answer("""Как вас зовут?""")
    await state.set_state(RegistrationForm.name)


@default_router.message(F.text == "Отменить")
async def process_cancel(message: Message, state: FSMContext):
    await state.clear()

    await message.answer("""Начнем с самого начала начала.\nКак вас зовут?""", reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationForm.name)
