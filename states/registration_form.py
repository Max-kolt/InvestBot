from aiogram.fsm.state import StatesGroup, State


class RegistrationForm(StatesGroup):
    name = State()
    project_description = State()
    amount_of_income = State()
    required_amount = State()
    # amount_purpose = State()
    document = State()
    necessary_assistance = State()

