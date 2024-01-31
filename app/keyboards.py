from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_keyboard(btns: list[str]):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for btn in btns:
        kb.add(KeyboardButton(btn))
    return kb
