import asyncio
import logging
import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Update

from config import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PATH
from handlers import start_handler, file_handler, payment_handler, receipts, cancel_handler
from cleaner_unpaid import clean_unpaid_files

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

dp.include_router(start_handler.router)
dp.include_router(file_handler.router)
dp.include_router(payment_handler.router)
dp.include_router(receipts.router)
dp.include_router(cancel_handler.router)

app = FastAPI()

@app.on_event("startup")
async def on_startup() -> None:
    if WEBHOOK_URL:
        await bot.set_webhook(WEBHOOK_URL + WEBHOOK_PATH)
    asyncio.create_task(clean_unpaid_files())

@app.on_event("shutdown")
async def on_shutdown() -> None:
    await bot.session.close()

@app.post(WEBHOOK_PATH)
async def handle_webhook(request: Request):
    update = Update.model_validate(await request.json())
    await dp.feed_update(bot, update)
    return {"ok": True}
