from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def confirmation_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Так")],
        [KeyboardButton(text="Ні")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
