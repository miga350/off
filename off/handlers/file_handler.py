from aiogram import Router, F
from aiogram.types import Message
from aiogram.types.input_file import BufferedInputFile
import os

router = Router()

@router.message(F.document)
async def handle_file(msg: Message):
    doc = msg.document
    if not doc.file_name.endswith(".pdf"):
        await msg.answer("❌ Разрешены только PDF-файлы.")
        return

    if doc.file_size > 20 * 1024 * 1024:
        await msg.answer("❌ Размер файла не должен превышать 20 МБ.")
        return

    file = await msg.bot.get_file(doc.file_id)
    file_path = f"temp_uploads/{msg.from_user.id}_{doc.file_name}"
    await msg.bot.download_file(file.file_path, destination=file_path)
    await msg.answer("✅ Файл получен. Теперь оплатите услугу, чтобы начать проверку.")
