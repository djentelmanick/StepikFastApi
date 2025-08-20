import os
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from itsdangerous import Signer
from main import app


client = TestClient(app)

# Тестовые данные
TEST_USERNAME = "testuser"
TEST_PASSWORD = "testpass"
SECRET_KEY = os.getenv("SECRET_KEY")  # Должен совпадать с ключом в приложении


def test_login_success():
    """Тест успешного логина и установки cookie"""
    response = client.post("/login", json={"username": TEST_USERNAME, "password": TEST_PASSWORD})

    assert response.status_code == 200
    assert response.json() == {"message": "Cookie has been set"}

    # Проверяем, что cookie установлена
    cookie = response.cookies.get("session_token")
    assert cookie is not None

    # Проверяем формат cookie: <user_id>.<signature>
    parts = cookie.split(".")
    assert len(parts) == 2
    try:
        UUID(parts[0])  # Проверяем, что первая часть - валидный UUID
    except ValueError:
        pytest.fail("Invalid UUID in session token")


def test_profile_access_with_valid_cookie():
    """Тест доступа к /profile с валидной cookie"""
    # Сначала логинимся
    login_response = client.post("/login", json={"username": TEST_USERNAME, "password": TEST_PASSWORD})
    cookie = login_response.cookies.get("session_token")

    # Запрашиваем профиль с cookie
    response = client.get("/profile", cookies={"session_token": cookie})

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == TEST_USERNAME
    assert "user_id" in data


def test_profile_access_without_cookie():
    """Тест доступа к /profile без cookie"""
    no_cookies_client = TestClient(app)

    response = no_cookies_client.get("/profile")
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


def test_profile_access_with_invalid_cookie():
    """Тест доступа к /profile с поддельной cookie"""
    # Генерируем невалидную подпись с другим ключом
    fake_signer = Signer("wrong-secret-key")
    fake_token = fake_signer.sign("fake-user-id").decode("utf-8")

    response = client.get("/profile", cookies={"session_token": fake_token})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid session token"


def test_cookie_httponly():
    """Тест, что cookie помечена как HttpOnly"""
    response = client.post("/login", json={"username": TEST_USERNAME, "password": TEST_PASSWORD})

    set_cookie_header = response.headers.get("set-cookie", "").lower()
    assert "httponly" in set_cookie_header
