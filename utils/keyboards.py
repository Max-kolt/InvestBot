from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Заново зарегистрироваться"), KeyboardButton(text="Записаться на встречу")]
], resize_keyboard=True)

