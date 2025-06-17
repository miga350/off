from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.lower() == "🧾 мои чеки")
async def receipts_handler(msg: Message):
    await msg.answer("Пока что тут будет список ваших чеков.")
