from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext

from states import CallScheduleForm
from utils import week_schedule_generate


meet_selection_router = Router(name="MeetSelection")


@meet_selection_router.callback_query(F.data == "select_meet_time")
# @meet_selection_router.message(F.text)
async def start_scheduling(call: CallbackQuery, state: FSMContext):
    await state.set_state(CallScheduleForm.week_day)
    # keyboard_message = await message.answer("", reply_markup=ReplyKeyboardMarkup(
    #     keyboard=[[KeyboardButton(text="Отмена")]]
    # ))
    # print(keyboard_message)
    # await keyboard_message.delete()
    await call.message.answer(
        'Выберите день:',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=day, callback_data=f"sched_{day}")] for day in week_schedule_generate()
        ])
    )

