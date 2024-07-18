from os import getenv
from dotenv import load_dotenv

load_dotenv()


TOKEN = getenv("TOKEN")
DB_NAME = getenv("DB_NAME")

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

ADMIN = 'runit_mak'
