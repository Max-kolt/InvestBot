from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, \
    KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import Filter
from aiogram.methods.send_message import SendMessage
from loguru import logger

from states import CallScheduleForm
from utils import week_schedule_generate, send_to_admin
from config import DEFAULT_DAY_SCHEDULE


meet_selection_router = Router(name="MeetSelection")


@meet_selection_router.callback_query(F.data == "select_meet_time")
async def start_scheduling(call: CallbackQuery, state: FSMContext):
    await state.set_state(CallScheduleForm.week_day)
    await call.message.answer(
        'Выберите день',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=day, callback_data=f"sched_day_{day}")]
            for day in week_schedule_generate()
        ])
    )


@meet_selection_router.callback_query(CallScheduleForm.week_day, F.data.startswith("sched_day_"))
async def process_day_schedule(call: CallbackQuery, state: FSMContext):
    current_day = call.data.split("_")[-1]
    await state.update_data(week_day=current_day)
    await state.set_state(CallScheduleForm.day_time)
    await call.message.delete()
    await call.message.answer(text=current_day, reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text='Отмена')]
    ]))
    await call.message.answer(
        "Выберите время",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"{hour}:00", callback_data=f"sched_hour_{hour}")]
            for hour in DEFAULT_DAY_SCHEDULE
        ])
    )


@meet_selection_router.callback_query(CallScheduleForm.day_time, F.text == "Отмена")
async def process_cancel_schedule(message: Message, state: FSMContext):
    await state.clear()
    await message.delete()
    await message.delete()
    await message.answer(text='Запись отменена', reply_markup=ReplyKeyboardRemove())


@meet_selection_router.callback_query(CallScheduleForm.day_time, F.data.startswith("sched_hour_"))
async def process_hour_chedule(call: CallbackQuery, state: FSMContext, bot: Bot):
    current_hour = call.data.split('_')[-1]
    await state.update_data(day_time=current_hour)
    data = await state.get_data()
    await send_to_admin(bot, text=f"#{call.from_user.id} \nПользователь {call.from_user.username} запланировал встречу на {data['week_day']} "
                        f"в {data['day_time']}:00")
    await state.clear()
    logger.info(f"User {call.from_user.username} schedule meeting: {data['week_day']}, {data['day_time']}:00")
    await call.message.answer("Благодарю за запись. Накануне онлайн-встречи я пришлю вам ссылку на встречу. Следите "
                              "за уведомлениями!")




