from aiogram import Router, F
from aiogram.types import Message
from datetime import datetime
from database.db import SessionLocal
from database.models import Receipt, StatusEnum

router = Router()

@router.message(F.text.lower() == "🧾 мои чеки")
async def receipts_handler(msg: Message):
    async with SessionLocal() as session:
        result = await session.execute(
            Receipt.__table__.select().where(
                Receipt.user_id == msg.from_user.id,
                Receipt.status == StatusEnum.paid,
                Receipt.expires_at > datetime.utcnow(),
            )
        )
        records = result.fetchall()

    if not records:
        await msg.answer("У вас нет сохранённых чеков.")
        return

    lines = ["Ваши чеки:"]
    for r in records:
        if r.receipt_url:
            lines.append(r.receipt_url)

    await msg.answer("\n".join(lines))
