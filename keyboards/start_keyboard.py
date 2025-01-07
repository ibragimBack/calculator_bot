from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def choose_start_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Mbank MPlus'),
                KeyboardButton(text='Рассрочка без банка'),
            ]
        ]
    )
    return kb 