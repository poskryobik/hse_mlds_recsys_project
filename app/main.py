from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from typing import List
from pydantic import BaseModel
import pickle
import pandas as pd
from app.models.LFM import LFM
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
import datetime


app = FastAPI()

# Загрузка модели
with open("app/models/lfm_model.pkl", "rb") as f:
    model = pickle.load(f)
# Загрузка кодировщика
with open("app/models/encoder.pkl", "rb") as f:
    encoder = pickle.load(f)

# Загрузка данных
rating_df = pd.read_csv("app/ratings.csv", sep=',', encoding='utf-8')
products_df = pd.read_csv("app/products.csv", sep=',', encoding='utf-8')
# Инициализация модели
lfm_model = LFM(model=model, rating_df=rating_df, encoder=encoder)


@app.get("/")
@cache(expire=60)
async def greetings():
    """
        Ручка для приветсвия
    """
    return "Hello! This API for ML Service"


@app.on_event("startup")
async def startup():
    """
        Инициализация Redis
    """
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


class User(BaseModel):
    uid: int


@app.get("/personal_reccomend")
@cache(expire=120)  # Кеширование 2 минуты
def get_personal_reccom(user: User):
    """
        Персональная рекомендация
        (с кешированием 2 мин.)
    """
    items = lfm_model.recommend(uid=user.uid, k=10)
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
    prediction = lfm_model.predict(users_to_recommend=users_ids, k=10)
    lst_product = list(map(
        lambda x: products_df[
            products_df["product_id"].isin(x)]["product_name"].to_list(),
        prediction.values()))
    prediction = dict(zip(prediction.keys(), lst_product))
    prediction = dict(map(lambda x: (str(x[0]), x[1]), prediction.items()))
    return prediction


@app.post("/upload_multiple_reccomend")
def create_upload_file(file: UploadFile):
    """
        на вход подается csv-файл с uid клиентов,
        на выходе получаем файл с +1 столбцом - k продуктов
    """
    df = pd.read_csv(file.file, index_col=0)
    users_ids = list(df["user_id"].unique())
    prediction = lfm_model.predict(users_to_recommend=users_ids, k=10)
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
