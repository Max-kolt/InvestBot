from aiogram.fsm.state import State, StatesGroup


class SendPostForm(StatesGroup):
    post = State()
