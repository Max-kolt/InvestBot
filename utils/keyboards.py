from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Записаться на встречу"),
     KeyboardButton(text="Получить подарок")],
    [KeyboardButton(text="Заново зарегистрироваться")]
], resize_keyboard=True)

start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Получить подарок")],
    [KeyboardButton(text="Записаться на консультацию")]
], resize_keyboard=True)

admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="/send_all_users"),
     KeyboardButton(text="/get_utm")],
], resize_keyboard=True)
