from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from bot.filters.find_uid import HasUidFilter
from typing import List
import requests
from bot.handlers.markup import main_keyboard, make_row_keyboard


router = Router()
person_reccom = "Одному пользователю"
multiple_reccom = "Списку пользователей"
cold_start = "Холодный старт"


def get_reccom_str(products_names: list):
    """
        Строка для персональной рекомендации
    """
    ans_str = "".join([str(i+1) + ": " + str(product) + "\n"
                       for i, product in enumerate(products_names)])
    return ans_str


def get_multiple_reccom_str(reccomendation):
    """
        Строка для множественной рекомендации
    """
    ans_str = "".join([str(k) + ": " + str(val) + "\n"
                       for k, val in reccomendation.items()])
    return ans_str


class Reccom(StatesGroup):
    """
        Состояния конечного автомата
    """
    choosing_reccom = State()
    choosing_uid = State()


@router.message(Command("reccom"))
async def cmd_reccom(message: Message, state: FSMContext):
    """
        Формирование клавиатуры и начало рекомендаций
    """
    await message.answer(
        text="Выберете способ рекомендации:",
        reply_markup=make_row_keyboard()
    )
    await state.set_state(Reccom.choosing_reccom)


@router.message(F.text.lower() == "рекомендации")
async def msg_cmd_reccom(message: Message, state: FSMContext):
    """
        Формирование клавиатуры и начало рекомендаций
    """
    await message.answer(
        text="Выберете способ рекомендации:",
        reply_markup=make_row_keyboard()
    )
    await state.set_state(Reccom.choosing_reccom)

@router.message(Reccom.choosing_reccom, F.text.in_(person_reccom))
async def reccom_chosen(message: Message, state: FSMContext):
    """
        Запрос uid для персональной рекомендации
    """
    await state.update_data(chosen_reccom=message.text.lower())
    await message.answer(
        text="Пожалуйста, введите uid пользователя:",
        reply_markup=ReplyKeyboardRemove())
    await state.set_state(Reccom.choosing_uid)


@router.message(Reccom.choosing_reccom, F.text.in_(multiple_reccom))
async def reccoms_chosen(message: Message, state: FSMContext):
    """
        Запрос списка uid для множественной рекомендации
    """
    await state.update_data(chosen_reccom=message.text.lower())
    await message.answer(
        text="Пожалуйста, введите список с uid пользователей:",
        reply_markup=ReplyKeyboardRemove())
    await state.set_state(Reccom.choosing_uid)


@router.message(Reccom.choosing_reccom, F.text.in_(cold_start))
async def cold_reccom_chosen(message: Message, state: FSMContext):
    """
        Запрос списка продуктов для нового пользователя
    """
    await state.update_data(chosen_reccom=message.text.lower())
    await message.answer(
        text="Пожалуйста, введите список product_id нового пользователя:",
        reply_markup=ReplyKeyboardRemove())
    await state.set_state(Reccom.choosing_uid)



@router.message(Reccom.choosing_uid, HasUidFilter())
async def reccom_chosen_result(message: Message, state: FSMContext,
                               uids: List[str]):
    """
        Вернуть рекомендацию
        Осуществляется к развернутому FastAPI в рамках проекта
    """
    user_data = await state.get_data()

    if user_data['chosen_reccom'] == person_reccom.lower():
        data = {"uid": uids[0]}
        response = requests.get("http://fastapi_app:8000/personal_reccomend",
                                json=data)
        products = (response.json()[uids[0]]
                    .replace("[", "").replace("]", "").split(","))
        products_names = get_reccom_str(products_names=products)
        await message.answer(text=products_names, reply_markup=main_keyboard())
    elif user_data['chosen_reccom'] == multiple_reccom.lower():
        data = [{"uid": i} for i in uids]
        response = requests.get("http://fastapi_app:8000/multiple_reccomend",
                                json=data)
        prediction = dict(response.json())
        prediction = get_multiple_reccom_str(reccomendation=prediction)
        await message.answer(text=prediction, reply_markup=main_keyboard())
    elif user_data['chosen_reccom'] == cold_start.lower():
        data = [prodid for prodid in uids]
        response = requests.get("http://fastapi_app:8000/cold_start",
                                json=data)
        prediction = list(response.json())[0]
        await message.answer(text=str(prediction), reply_markup=main_keyboard())
    # Чистка состояний
    await state.clear()


@router.message(Reccom.choosing_uid, F.text)
async def food_chosen_incorrectly(message: Message):
    """
        Когда нет цифр в исходном тексте
    """
    await message.answer(text="""В тексте не найдено ни одного uid.
Пожалуйста, попробуйте еще раз""")
