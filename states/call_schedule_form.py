from aiogram.fsm.state import StatesGroup, State


class CallScheduleForm(StatesGroup):
    week_day = State()
    day_time = State()
