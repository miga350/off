from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from database.db import SessionLocal
from database.models import User
from keyboards import get_accept_keyboard, get_main_keyboard, get_cancel_keyboard
from states import CheckPDFStates

router = Router()

@router.message(commands=["start"])
async def start_command(message: types.Message, state: FSMContext):
    async with SessionLocal() as session:
        user = await session.get(User, message.from_user.id)
        if not user:
            user = User(user_id=message.from_user.id)
            session.add(user)
            await session.commit()
            await session.refresh(user)

        if not user.accepted_terms:
            await message.answer(
                "🔐 Для продолжения нужно принять условия политики и оферты.",
                reply_markup=get_accept_keyboard()
            )
        else:
            await message.answer("👋 Добро пожаловать!", reply_markup=get_main_keyboard())

@router.message(lambda msg: msg.text == "✅ Принять условия")
async def accept_terms(message: types.Message, state: FSMContext):
    async with SessionLocal() as session:
        user = await session.get(User, message.from_user.id)
        if user and not user.accepted_terms:
            user.accepted_terms = True
            await session.commit()
            await message.answer("Спасибо, вы приняли условия.", reply_markup=get_main_keyboard())


@router.message(lambda msg: msg.text == "📤 Загрузить файл")
async def upload_prompt(message: types.Message, state: FSMContext):
    await message.answer(
        "Пришлите PDF-файл для проверки (не более 20 МБ) или нажмите \"Отмена\".",
        reply_markup=get_cancel_keyboard(),
    )
    await state.set_state(CheckPDFStates.waiting_file)
