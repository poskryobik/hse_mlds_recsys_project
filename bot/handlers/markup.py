from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_keyboard() -> ReplyKeyboardMarkup:
    """
        Формирование клавиатуры для главного меню
    """
    kb = [[
            KeyboardButton(text="Рекомендации"),
            KeyboardButton(text="Оценить бота"),
            KeyboardButton(text="Статистика бота")
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard


def make_row_keyboard() -> ReplyKeyboardMarkup:
    """
        Формирование клавиатуры для рекомендации
    """
    kb = [[
            KeyboardButton(text="Одному пользователю"),
            KeyboardButton(text="Списку пользователей"),
            KeyboardButton(text="Холодный старт")
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ рекомендации"
    )
    return keyboard
