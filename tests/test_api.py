import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from typing import AsyncGenerator
from app.main import app
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
import os


client = TestClient(app=app)
# Инициализация базы для кеширования
redis = aioredis.from_url("redis://localhost")
FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


# Фикстура для асинхронных ручек
@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# тест синхронной ручки ping
def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200


# тест асинхронной ручки "/" с фикстурой
@pytest.mark.asyncio
async def test_root(async_client: AsyncClient):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello! This API for ML Service"


@pytest.mark.parametrize("json", [{"uid": "1"},
                                  {"uid": "2024"},
                                  {"uid": "9999"}])
def test_personal_reccomend(json):
    """
        Тест ручки с рекомендацией
        для одного пользователя
    """
    response = client.request(method="get",
                              url="/personal_reccomend",
                              json=json)
    assert response.status_code == 200


@pytest.mark.parametrize("json", [[{"uid": "1"}, {"uid": "2024"}],
                                  [{"uid": "100"}, {"uid": "9999"}]])
def test_multiple_reccomend(json):
    """
        Тест ручки с рекомендациями
        для списка пользователей
    """
    response = client.request(method="get",
                              url="/multiple_reccomend",
                              json=json)
    assert response.status_code == 200


def test_upload_multiple_reccomend():
    """
        Тест рчки с рекомендациями
        для csv с пользователями
    """
    with open("app/test.csv", "rb") as f:
        response = client.request(method="post",
                                  url="/upload_multiple_reccomend",
                                  files={"file": ("test", f, "csv")})
    assert response.status_code == 200


# Удаление файлов необходимых тестов
os.remove("app/models/encoder.pkl")
os.remove("app/models/lfm_model.pkl")
os.remove("app/ratings.csv")
os.remove("app/products.csv")
