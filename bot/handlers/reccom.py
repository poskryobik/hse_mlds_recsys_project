from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from filters.find_uid import HasUidFilter
from typing import List
from LFM import LFM
import pandas as pd
import pickle


# Загрузка модели
with open("lfm_model.pkl", "rb") as f:
    model = pickle.load(f)
# Загрузка кодировщика
with open("encoder.pkl", "rb") as f:
    encoder = pickle.load(f)
# Загрузка данных
rating_df = pd.read_csv("ratings.csv", index_col=0)
products_df = pd.read_csv("products.csv")
# Инициализация модели
lfm_model = LFM(model=model, rating_df=rating_df, encoder=encoder)



router = Router()

person_reccom = "Одному пользователю"
multiple_reccom = "Списку пользователей"

def make_row_keyboard() -> ReplyKeyboardMarkup:
    """
        Формирование клавиатуры для рекомендации
    """
    kb = [[
            KeyboardButton(text="Одному пользователю"),
            KeyboardButton(text="Списку пользователей")
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ рекомендации"
    )
    return keyboard

def get_reccom_str(products_names: list):
    """
        Строка для персональной рекомендации
    """
    ans_str = "".join([str(i+1) + ": " + str(product) + "\n" for i, product in enumerate(products_names)])
    return ans_str

def get_multiple_reccom_str(reccomendation):
    """
        Строка для множественной рекомендации
    """
    ans_str = "".join([str(k) + ": " + str(val) + "\n" for k, val in reccomendation.items()])
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
async def reccom_chosen(message: Message, state: FSMContext):
    """
        Запрос списка uid для множественной рекомендации
    """
    await state.update_data(chosen_reccom=message.text.lower())
    await message.answer(
        text="Пожалуйста, введите список с uid пользователей:",
        reply_markup=ReplyKeyboardRemove())
    await state.set_state(Reccom.choosing_uid)




@router.message(Reccom.choosing_uid, HasUidFilter())
async def reccom_chosen_result(message: Message, state: FSMContext, uids: List[str]):
    """
        Вернуть рекомендацию
    """
    user_data = await state.get_data()

    if user_data['chosen_reccom'] == person_reccom.lower():
        items = lfm_model.recommend(uid=uids[0], k=10)
        products_names = products_df[products_df["product_id"].isin(items)]["product_name"].to_list()
        products_names = get_reccom_str(products_names=products_names)
        await message.answer(text = products_names)
    elif user_data['chosen_reccom'] == multiple_reccom.lower():
        prediction = lfm_model.predict(users_to_recommend=uids, k=10)
        prediction = (dict(zip(prediction.keys(), 
                            list(map(lambda x: products_df[products_df["product_id"].isin(x)]["product_name"].to_list(), 
                                        prediction.values())))))
        prediction = get_multiple_reccom_str(reccomendation=prediction)
        await message.answer(text = prediction)
    # Чистка состояний
    await state.clear()
    

@router.message(Reccom.choosing_uid, F.text)
async def food_chosen_incorrectly(message: Message):
    """
        Когда нет цифр в исходном тексте 
    """
    await message.answer(text="В тексте не найдено ни одного uid, пожалуйста, попробуйте еще раз")


