import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from loguru import logger

from config import TOKEN
from database import db
from routers import all_routers

dp = Dispatcher()
logger.add('app_logger.log', rotation="500 MB", compression="gz", level="DEBUG", diagnose=False, backtrace=False)


async def main():
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    db.connect()
    dp.include_routers(*all_routers)
    logger.info("Bot has been started")

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

