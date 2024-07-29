from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Записаться на встречу"),
    KeyboardButton(text="Получить подарок")],
    [KeyboardButton(text="Заново зарегистрироваться")]
], resize_keyboard=True)

