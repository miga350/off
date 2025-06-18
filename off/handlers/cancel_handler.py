from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import os
from keyboards import get_main_keyboard

router = Router()

@router.message(F.text == "❌ Отмена")
async def cancel_handler(msg: Message, state: FSMContext):
    data = await state.get_data()
    file_path = data.get('file_path')
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
        except OSError:
            pass
    await state.clear()
    await msg.answer("Действие отменено.", reply_markup=get_main_keyboard())
