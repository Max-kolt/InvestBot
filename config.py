import os
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv("TOKEN")


DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_USER_PASSWORD = os.getenv('DB_USER_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT', "5432"))

DEFAULT_WEEK_SCHEDULE = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
DEFAULT_DAY_SCHEDULE = [12, 13, 14, 15, 16, 17]

DEFAULT_NECESSARY_ASSISTANCE = {
    "counseling": "Консультация инвестора",
    "presentation": "Презентация для инвесторов",
    "resume": "Резюме проекта (тизер)",
    "business": "Бизнес-план",
    "model": "Финансовая модель",
    "contract": "Шаблон договора с инвестором",
    "report": "Финансовый отчет за прошедший период"
}

# ADMIN = -4252150781
ADMIN = -1002178066934

CHANNEL_NAME = "atlantcapital_free"
CHANNEL_LINK = f"https://t.me/{CHANNEL_NAME}"
