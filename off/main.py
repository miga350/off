import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from handlers import start_handler, upload_handler, payment_handler, check_handler
from cleaner_unpaid import clean_unpaid_files
import logging
import os

from config import BOT_TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Регистрация хендлеров
dp.include_router(start_handler.router)
dp.include_router(upload_handler.router)
dp.include_router(payment_handler.router)
dp.include_router(check_handler.router)

async def main():
    # Запуск фоновой задачи по автоудалению неоплаченных PDF
    asyncio.create_task(clean_unpaid_files())

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
