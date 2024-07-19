from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, \
    KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.methods import GetFile
import aiohttp
from loguru import logger
import asyncio

from config import DEFAULT_NECESSARY_ASSISTANCE
from states import RegistrationForm
from database import Investor
from utils import send_to_admin

registration_router = Router(name="Registration")


@registration_router.message(F.text == "Отменить")
async def process_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("""Начнем с самого начала начала.\nКак вас зовут?""", reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationForm.name)


@registration_router.message(RegistrationForm.name)
async def process_name(message: Message, state: FSMContext):
    name = message.text.casefold().title()
    await state.update_data(name=name)
    await state.set_state(RegistrationForm.project_description)
    await message.answer(
        """Опишите ваш бизнес проект в 1 предложении.""",
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [KeyboardButton(text="Отменить")]
        ])
    )


@registration_router.message(RegistrationForm.project_description)
async def process_description(message: Message, state: FSMContext):
    project_description = message.text.casefold()
    await state.update_data(project_description=project_description)
    await state.set_state(RegistrationForm.amount_of_income)
    await message.answer("Какой размер выручки у вас на текущий момент?\n"
                         "Если у вас только идея, спокойно пишите 0, такое тоже возможно.")


@registration_router.message(RegistrationForm.amount_of_income)
async def process_income_amount(message: Message, state: FSMContext):
    amount = message.text.casefold()
    await state.update_data(amount_of_income=amount)
    await state.set_state(RegistrationForm.required_amount)
    await message.answer("""Какую сумму вы хотели привлечь?""")


@registration_router.message(RegistrationForm.required_amount)
async def process_required_amount(message: Message, state: FSMContext):
    needed_amount = message.text.casefold()
    await state.update_data(required_amount=needed_amount)
    await state.set_state(RegistrationForm.document)
    await message.answer(
        "Прикрепите документы, которые у вас есть по проекту – презентация, "
        "фин модель, бизнес-план, если нет, тоже не страшно",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Без документа", callback_data="without_document")]
            ]
        )
    )


@registration_router.callback_query(RegistrationForm.document, F.data == "without_document")
async def process_without_document(call: CallbackQuery, state: FSMContext):
    await state.update_data(document=False)
    await state.set_state(RegistrationForm.necessary_assistance)
    await call.message.delete()
    await call.message.answer(
        """Какая помощь в подготовке вам может потребоваться, выберите:""",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=assist, callback_data=f"assist_{i}")] for i, assist in
                DEFAULT_NECESSARY_ASSISTANCE.items()
            ]
        )
    )


@registration_router.message(RegistrationForm.document, F.document)
async def process_document(message: Message, state: FSMContext):
    file_id = message.document.file_id
    await state.update_data(document=file_id)
    await state.set_state(RegistrationForm.necessary_assistance)
    await message.answer(
        """Какая помощь в подготовке вам может потребоваться, выберите:""",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=assist, callback_data=f"assist_{i}")] for i, assist in
                DEFAULT_NECESSARY_ASSISTANCE.items()
                # [InlineKeyboardButton(text="Консультация инвестора", callback_data="assist_counseling")],
                # [InlineKeyboardButton(text="Презентация для инвесторов", callback_data="assist_presentation")],
                # [InlineKeyboardButton(text="Резюме проекта (тизер)", callback_data="assist_resume")],
                # [InlineKeyboardButton(text="Бизнес-план", callback_data="assist_business")],
                # [InlineKeyboardButton(text="Финансовая модель", callback_data="assist_model")],
                # [InlineKeyboardButton(text="Шаблон договора с инвестором", callback_data="assist_contract")],
                # [InlineKeyboardButton(text="Финансовый отчет за прошедший период", callback_data="assist_report")]
            ]
        )
    )


@registration_router.callback_query(RegistrationForm.necessary_assistance, F.data.startswith("assist_"))
async def process_assistance(call: CallbackQuery, state: FSMContext, bot: Bot):
    assist_data = call.data.split('_')[-1]
    await state.update_data(necessary_assistance=DEFAULT_NECESSARY_ASSISTANCE[assist_data])
    data = await state.get_data()
    # if Investor.select().where(Investor.login == call.from_user.username):
    #     (Investor.delete().where(Investor.login == call.from_user.username)).execute()
    #     logger.info(f"Delete old {call.from_user.username} info")
    # Investor.create(**data, login=call.from_user.username, chat_id=call.from_user.id)
    #     name=data['name'], project_description=data["project_description"],
    #     amount_of_income=data["amount_of_income"],
    #     required_amount=data["required_amount"],
    #     document=data["document"] if not data["document"] else "",
    #     necessary_assistance=data["necessary_assistance"],
    #     login=call.from_user.username, chat_id=call.from_user.id
    # )

    logger.info(f"User {call.from_user.username} registered")
    await send_to_admin(
        bot,
        text=f"#{call.from_user.id} \nНовый пользователь: {call.from_user.username}\n"
             f"Имя: {data['name']}\nОписание проекта: {data['project_description']}\n"
             f"Размер выручки: {data['amount_of_income']}\nНеобходимо привлечь: {data['required_amount']}\n"
             f"Требуемая помощь: {data['necessary_assistance']}",
        document=data['document']
    )
    await state.clear()
    await call.message.delete()
    await call.message.answer("Мы рады что вы с нами, нам уже нравится ваш проект!", reply_markup=ReplyKeyboardRemove())
    await call.message.answer(
        "Предлагаю назначить всречу с учредителями Atlant Capital, "
        "чтобы обсудить детали дальнейшей работы по вашему проекту.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Выбрать время встречи", callback_data="select_meet_time")]
            ]
        )
    )
