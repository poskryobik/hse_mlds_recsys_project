from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from typing import List
from pydantic import BaseModel
import pandas as pd
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
import datetime
import torch
import pickle
from app.models.models import EncoderRNN, DecoderRNN
from app.models.next_basket import NextBasket


app = FastAPI()

MAX_LENGTH = 630

products_df = pd.read_csv("app/models/products.csv", sep=',', encoding='utf-8')
last_basket = pd.read_parquet("app/models/users_baskets.parquet")

with open('app/models/product_to_id.pickle', 'rb') as handle:
    product_to_id = pickle.load(handle)
with open('app/models/user_to_id.pickle', 'rb') as handle:
    user_to_id = pickle.load(handle)
with open('app/models/id_to_product.pickle', 'rb') as handle:
    id_to_product = pickle.load(handle)
with open('app/models/top_product.pickle', 'rb') as handle:
    top_product = pickle.load(handle)

device = 'cpu'
# Инициализация моделей
hidden_size = 128
encoder0 = EncoderRNN(len(product_to_id.keys())+3, hidden_size,
                      device).to(device)
decoder0 = DecoderRNN(hidden_size, len(product_to_id.keys())+3,
                      device).to(device)
# Загрузка весов обученной модели
encoder0.load_state_dict(torch.load("app/models/encoder_1.pt",
                                    map_location=torch.device(device)))
decoder0.load_state_dict(torch.load("app/models/decoder_1.pt",
                                    map_location=torch.device(device)))

model = NextBasket(encoder=encoder0, decoder=decoder0, device=device,
                   prod_to_id=product_to_id, user_to_id=user_to_id,
                   id_to_product=id_to_product, top_product=top_product,
                   df=last_basket, max_length=MAX_LENGTH)


@app.on_event("startup")
async def startup():
    """
        Инициализация Redis
    """
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.get("/")
async def greetings():
    """
        Ручка для приветсвия
    """
    return "Hello! This API for ML Service"


class User(BaseModel):
    uid: int


@app.get("/personal_reccomend")
@cache(expire=120)  # Кеширование 2 минуты
def get_personal_reccom(user: User):
    """
        Персональная рекомендация
        (с кешированием 2 мин.)
    """
    items = model.recommend(user_id=user.uid, k=10)
    products_name = (
        products_df[products_df["product_id"].isin(items)]
        ["product_name"].to_list())
    return {f"{user.uid}": f"{products_name}"}


@app.get("/multiple_reccomend")
@cache(expire=120)  # Кеширование 2 минуты
def get_multiple_reccom(users: List[User]):
    """
        Для списка пользователей возвращает рекомендации
        (с кешированием 2 мин.)
    """
    users_ids = [user.uid for user in users]
    prediction = model.predict(users_to_recommend=users_ids, k=10)
    lst_product = list(map(
        lambda x: products_df[
            products_df["product_id"].isin(x)]["product_name"].to_list(),
        prediction.values()))
    prediction = dict(zip(prediction.keys(), lst_product))
    prediction = dict(map(lambda x: (str(x[0]), x[1]), prediction.items()))
    return prediction


@app.get("/cold_start")
@cache(expire=120)  # Кеширование 2 минуты
def get_cold_start(products: List[int]):
    """
        Для списка пользователей возвращает рекомендации
        (с кешированием 2 мин.)
    """
    # products_ids = [prod.uid for prod in products]
    items = model.cold_start(cold_seq=products, k=10)
    products_name = (
        products_df[products_df["product_id"].isin(items)]
        ["product_name"].to_list())
    return {f"{products_name}"}


@app.post("/upload_multiple_reccomend")
def create_upload_file(file: UploadFile):
    """
        на вход подается csv-файл с uid клиентов,
        на выходе получаем файл с +1 столбцом - k продуктов
    """
    df = pd.read_csv(file.file, index_col=0)
    users_ids = list(df["user_id"].unique())
    prediction = model.predict(users_to_recommend=users_ids, k=10)
    lst_product = list(map(
        lambda x: products_df[
            products_df["product_id"].isin(x)]["product_name"].to_list(),
        prediction.values()))
    prediction = dict(zip(prediction.keys(), lst_product))
    rec_df = pd.DataFrame(prediction.items(),
                          columns=["user_id", "reccomendation"])
    df = df.merge(rec_df, on="user_id", how="left")
    df.to_csv("multiple_reccomend.csv")
    return FileResponse("multiple_reccomend.csv",
                        media_type="text/csv",
                        filename=file.filename)


@app.get("/ping")
async def ping():
    """
        Проверка доступности сервера
    """
    now = datetime.datetime.now()
    return f"Server is available. Server date: {now}"
