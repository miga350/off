from aiogram import Router, F
from aiogram.types import Message, LabeledPrice
from config import BOT_TOKEN, SHOP_ID
from yookassa_api import get_receipt_url

router = Router()

@router.message(F.text.lower() == "💳 оплатить")
async def send_invoice(msg: Message):
    await msg.bot.send_invoice(
        msg.chat.id,
        title="Проверка PDF-документа на наличие ЭП",
        description="После оплаты документ будет проверен и вы получите чек.",
        provider_token=BOT_TOKEN,
        currency="RUB",
        prices=[LabeledPrice(label="Проверка PDF-документа на наличие ЭП", amount=49900)],
        start_parameter="check_pdf",
        payload=str(msg.from_user.id)
    )

@router.message(F.successful_payment)
async def success_payment(msg: Message):
    payment_id = msg.successful_payment.invoice_payload
    receipt_url = await get_receipt_url(payment_id)
    if receipt_url:
        await msg.answer(f'🧾 Ваш чек: {receipt_url}')
    else:
        await msg.answer('⚠️ Чек не удалось получить. Свяжитесь с поддержкой.')
