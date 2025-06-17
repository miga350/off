from aiogram import Router, F
from aiogram.types import Message, LabeledPrice
from aiogram.fsm.context import FSMContext
from config import YOOKASSA_SECRET, SHOP_ID
from yookassa_api import get_receipt_url
from states import CheckPDFStates
from pdf_utils import verify_signature, file_hash
from database.db import SessionLocal
from database.models import Receipt, StatusEnum

router = Router()

@router.message(CheckPDFStates.waiting_payment, F.text.lower() == "💳 оплатить")
async def send_invoice(msg: Message, state: FSMContext):
    await msg.bot.send_invoice(
        msg.chat.id,
        title="Проверка PDF-документа на наличие ЭП",
        description="После оплаты документ будет проверен и вы получите чек.",
        provider_token=YOOKASSA_SECRET,
        currency="RUB",
        prices=[LabeledPrice(label="Проверка PDF-документа на наличие ЭП", amount=49900)],
        start_parameter="check_pdf",
        payload=str(msg.from_user.id)
    )

@router.message(CheckPDFStates.waiting_payment, F.successful_payment)
async def success_payment(msg: Message, state: FSMContext):
    data = await state.get_data()
    file_path = data.get('file_path')
    payment_id = msg.successful_payment.provider_payment_charge_id

    result = verify_signature(file_path) if file_path else {'errors': ['no file']}
    receipt_url = await get_receipt_url(payment_id)

    async with SessionLocal() as session:
        rec = Receipt(
            user_id=msg.from_user.id,
            payment_id=payment_id,
            file_path=file_path or '',
            receipt_url=receipt_url,
            status=StatusEnum.paid,
        )
        session.add(rec)
        await session.commit()

    text = [
        'Результат проверки:',
        f"Подпись обнаружена: {'Да' if result.get('has_signature') else 'Нет'}",
        f"Подпись корректна: {'Да' if result.get('valid') else 'Нет'}",
    ]
    if result.get('signer'):
        text.append(f"Подписант: {result['signer']}")
    if receipt_url:
        text.append(f"Чек: {receipt_url}")
    if result.get('errors'):
        text.append('\n'.join(result['errors']))

    await msg.answer('\n'.join(text))
    await state.clear()
