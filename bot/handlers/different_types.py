from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.formatting import Text, Bold
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    """
        Обращение по имени
    """
    content = Text("Приветствую Вас, ", Bold(message.from_user.full_name), "!",
                   "\nЧтобы сделать рекомендацию введите /reccom",
                   "\nОценить работу бота /make_review",
                   "\nПросмотр графика отзывов /get_statistic"
                   )
    await message.answer(**content.as_kwargs())


@router.message(F.text)
async def message_with_text(message: Message):
    """
        В случае ввода какого либо сообщения вывод возможных команд
    """
    await message.answer("""Команда не ясна.
Пожалуйста, попробуйте ввести одну из команд:
/start - начало работы
/reccom - рекомендации для польтзователей
/make_review - оценить работу бота
/get_statistic - график статистики оценок""")


@router.message(F.sticker)
async def message_with_sticker(message: Message):
    """
        Информирование что прислали стикер
    """
    await message.answer("""Стикер не является командой.
Пожалуйста, введите команду.""")


@router.message(F.animation)
async def message_with_gif(message: Message):
    """
        Информирование что прислали GIF
    """
    await message.answer("""GIF не является командой.
Пожалуйста, введите команду.""")


@router.message(F.photo)
async def message_with_photo(message: Message):
    """
        Информирование что прислали изображение
    """
    await message.answer("""Изображение не является командой.
Пожалуйста, введите команду""")
