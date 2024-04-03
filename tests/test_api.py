import pytest
from fastapi.testclient import TestClient
from app.main import app
import os


client = TestClient(app=app)

def test_simple():
    assert 1 == 1

# тест ручки ping
def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200

# Удаление файлов необходимых тестов
os.remove("app/models/encoder.pkl")
os.remove("app/models/lfm_model.pkl")
os.remove("app/ratings.csv")
os.remove("app/products.csv")



