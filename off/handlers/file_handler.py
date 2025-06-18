from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import os
import time
from config import FILES_PATH

from keyboards import get_pay_keyboard
from states import CheckPDFStates

router = Router()

UPLOAD_FOLDER = FILES_PATH
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.message(CheckPDFStates.waiting_file, F.document)
async def handle_file(msg: Message, state: FSMContext):
    doc = msg.document
    if not doc.file_name.endswith(".pdf"):
        await msg.answer("❌ Разрешены только PDF-файлы.")
        return

    if doc.file_size > 20 * 1024 * 1024:
        await msg.answer("❌ Размер файла не должен превышать 20 МБ.")
        return

    telegram_file = await msg.bot.get_file(doc.file_id)
    file_path = os.path.join(UPLOAD_FOLDER, f"temp_{msg.from_user.id}_{int(time.time())}.pdf")
    await msg.bot.download_file(telegram_file.file_path, destination=file_path)
    await state.update_data(file_path=file_path)
    await state.set_state(CheckPDFStates.waiting_payment)
    await msg.answer(
        "✅ Файл получен, идёт подготовка к проверке. Для продолжения оплаты нажмите «Оплатить».",
        reply_markup=get_pay_keyboard(),
    )


