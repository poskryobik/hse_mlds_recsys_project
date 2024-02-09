from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, FSInputFile
import matplotlib.pyplot as plt
import seaborn as sns


def make_row_keyboard() -> ReplyKeyboardMarkup:
    """
        Клавиатура с оценками
    """
    row = [KeyboardButton(text=str(item)) for item in range(1, 6, 1)]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def calc_avg_grade(statistic_dict: dict):
    """
        Расчет среднего балла бота
    """
    sum_grade = 0
    count_grade = sum(list(statistic_dict.values()))
    for key in statistic_dict.keys():
        sum_grade += statistic_dict.get(key, 0) * float(key)
    if count_grade != 0:
        return sum_grade/count_grade
    else:
        return None


router = Router()


class BotStatistic(StatesGroup):
    """
        Состояния для конечного автомата
    """
    start_statistic = State()


@router.message(Command("make_review"))
async def mk_review(message: Message, state: FSMContext):
    """
        Клавиатура с оценками
    """
    await message.answer(
        text="Выберете оценку, которую заслжуил бот:",
        reply_markup=make_row_keyboard()
    )
    await state.set_state(BotStatistic.start_statistic)


@router.message(BotStatistic.start_statistic,
                F.text.in_([str(i) for i in range(1, 6, 1)]))
async def review(message: Message, state: FSMContext, statistic_dict):
    """
        Добавление оценок работы бота
    """
    await state.update_data(chosen_grade=message.text.lower())
    grade = message.text.lower()
    statistic_dict[grade] = statistic_dict.get(grade, 0) + 1
    await message.answer(
        text="Спасибо за отзыв, он учтен в статичстике бота!",
        reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(Command("get_statistic"))
async def mk_graph(message: Message, statistic_dict):
    """
        Формирование и отправка графика оценок
    """
    avg_grade = round(calc_avg_grade(statistic_dict), 2)
    plt.figure(figsize=(8, 4))
    sns.barplot(x=list(statistic_dict.keys()),
                y=list(statistic_dict.values()),
                label=f"Среняя оценка: {avg_grade}")
    plt.title("Оценки бота за время его работы")
    plt.xlabel("Оценка")
    plt.ylabel("Количество")
    plt.grid()
    plt.savefig("grade_graph.png")
    image_from_pc = FSInputFile("grade_graph.png")
    await message.answer_photo(
        image_from_pc,
        caption="Визуализация собранных оценок бота"
    )
