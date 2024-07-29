import asyncio

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, \
    KeyboardButton, ReplyKeyboardRemove, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Filter
from aiogram.methods.send_message import SendMessage
from aiogram.exceptions import TelegramNotFound
from loguru import logger
from datetime import date

from states import CallScheduleForm
from utils import week_schedule_generate, send_to_admin, day_schedule_generate, main_keyboard
from config import DEFAULT_DAY_SCHEDULE, DEFAULT_WEEK_SCHEDULE, CHANNEL_LINK, CHANNEL_NAME
from database import ScheduleTime, Investor, TimeTable

meet_selection_router = Router(name="MeetSelection")


# @meet_selection_router.message(F.text=='Записаться на встречу')
# async def start_scheduling(message: Message, state: FSMContext):
#     if ScheduleTime.select(Investor).join(Investor).where(ScheduleTime.investor.chat_id == message.from_user.id):


@meet_selection_router.message(F.text == "Записаться на встречу")
async def start_scheduling(message: Message, state: FSMContext):
    await state.set_state(CallScheduleForm.week_day)
    await message.answer(
        '🗓Выберите день встречи',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=day, callback_data=f"sched_day_{day}")]
            for day in week_schedule_generate()
        ])
    )


@meet_selection_router.callback_query(F.data == "select_meet_time")
async def start_scheduling(call: CallbackQuery, state: FSMContext):
    await state.set_state(CallScheduleForm.week_day)
    await call.message.answer(
        '🗓Выберите день встречи',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=day, callback_data=f"sched_day_{day}")]
            for day in week_schedule_generate()
        ])
    )


@meet_selection_router.callback_query(CallScheduleForm.week_day, F.data.startswith("sched_day_"))
async def process_day_schedule(call: CallbackQuery, state: FSMContext):
    # investor = ScheduleTime.select(ScheduleTime, Investor).join(Investor)\
    #     .where(Investor.chat_id == call.from_user.id).get()
    current_day = call.data.split("_")[-1]
    await state.update_data(day=current_day)
    await state.set_state(CallScheduleForm.day_time)
    await call.message.delete()
    await call.message.answer(
        text="🗓 "+current_day,
        # reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[KeyboardButton(text='Отмена')]])
    )
    await call.message.answer(
        "⏰Выберите время",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"{hour}:00", callback_data=f"sched_hour_{hour}")]
            for hour in day_schedule_generate(current_day.split(".")[0])
        ])
    )


@meet_selection_router.message(CallScheduleForm.day_time, F.text == "Отмена")
async def process_cancel_schedule(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text='Запись отменена', reply_markup=ReplyKeyboardRemove())


@meet_selection_router.callback_query(CallScheduleForm.day_time, F.data.startswith("sched_hour_"))
async def process_hour_schedule(call: CallbackQuery, state: FSMContext, bot: Bot):
    current_hour = call.data.split('_')[-1]
    await state.update_data(day_time=current_hour)
    await call.message.edit_text("⏰ "+current_hour + ":00")
    data = await state.get_data()
    current_date = date(day=int(data['day'].split(".")[0]), month=int(data['day'].split('.')[1]),
                        year=date.today().year)

    time = TimeTable.select() \
        .where(
        TimeTable.week_day == DEFAULT_WEEK_SCHEDULE[current_date.weekday()]
        and TimeTable.hours == data['day_time']
    ).get()
    investor = Investor.select().where(Investor.chat_id == call.from_user.id).get()

    ScheduleTime.create(week_time=time, investor=investor, date=current_date)

    await send_to_admin(bot,
                        text=f"#{call.from_user.id} \nПользователь {call.from_user.username} запланировал встречу на {data['day']} "
                             f"в {data['day_time']}:00")
    await state.clear()
    logger.info(f"User {call.from_user.username} schedule meeting: {data['day']}, {data['day_time']}:00")
    await call.message.answer("Благодарю за запись. Накануне онлайн-встречи я пришлю вам ссылку на встречу. Следите "
                              "за уведомлениями!", reply_markup=main_keyboard)

    if not Investor.select().where(Investor.get_gift, Investor.chat_id == str(call.from_user.id)):
        await asyncio.sleep(3)
        await call.message.answer("А пока мы готовимся к встрече предлагаю подписаться на наш канал!\n"
                                  "Там ты узнаешь:\n"
                                  "💫как не совершать ошибки при привлечении инвестиций, \n"
                                  "💫как масшибироваться легко, \n"
                                  "💫как общаться с инвесторами и многое другое \n\n"
                                  "В подарок за подписку тебя ждёт чек-лист, который поможет "
                                  "тебе на 70% быстрее привлечь инвестиции. \n\n"+CHANNEL_LINK,
                                  reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                      [InlineKeyboardButton(text="Получить подарок", callback_data="get_gift")]
                                  ])
                                  )

