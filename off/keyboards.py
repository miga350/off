from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📤 Загрузить файл")],
            [KeyboardButton(text="🧾 Мои чеки")],
            [KeyboardButton(text="💳 Оплатить")],
        ],
        resize_keyboard=True
    )

def get_accept_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Принять условия")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_pay_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="💳 Оплатить")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
