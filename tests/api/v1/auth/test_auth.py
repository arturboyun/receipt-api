import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.user.models import User
from tests.utils.random_name import get_random_name


@pytest.mark.asyncio
async def test_register_user(client: TestClient) -> None:
    data = {"username": get_random_name(), "password": "TestPassword123123", "name": get_random_name()}
    response = client.post("/api/v1/auth/register", json=data)
    assert response.status_code == 201
    response_data = response.json()
    assert "access_token" in response_data
    assert "refresh_token" not in response_data
    assert response_data["access_token"]
    assert response.cookies["refresh_token"]


@pytest.mark.asyncio
async def test_register_user_with_existing_username(client: TestClient) -> None:
    username = get_random_name()
    data = {"username": username, "password": "TestPassword123123", "name": "Test User"}
    response = client.post("/api/v1/auth/register", json=data)  # create user
    response = client.post("/api/v1/auth/register", json=data)  # try to create user with the same username
    assert response.status_code == 400
    response_data = response.json()
    assert response_data["detail"] == "User with this username already exists"


@pytest.mark.asyncio
async def test_login(client: TestClient) -> None:
    username = get_random_name()
    password = "TestPassword123123"

    data = {"username": username, "password": password, "name": "Test User"}
    response = client.post("/api/v1/auth/register", json=data)
    assert response.status_code == 201

    response = client.post("/api/v1/auth/token", data={"username": username, "password": password})
    response_data = response.json()
    assert "access_token" in response_data
    assert "refresh_token" not in response_data
    assert response_data["access_token"]
    assert response.cookies["refresh_token"]


@pytest.mark.asyncio
async def test_login_with_invalid_username(client: TestClient) -> None:
    response = client.post("/api/v1/auth/token", data={"username": "invalid_username", "password": "invalid_password"})
    assert response.status_code == 400
    response_data = response.json()
    assert response_data["detail"] == "Incorrect username or password"


@pytest.mark.asyncio
async def test_login_with_invalid_password(client: TestClient) -> None:
    username = get_random_name()
    password = "TestPassword123123"

    data = {"username": username, "password": password, "name": "Test User"}
    response = client.post("/api/v1/auth/register", json=data)
    assert response.status_code == 201

    response = client.post("/api/v1/auth/token", data={"username": username, "password": "invalid_password"})
    assert response.status_code == 400
    response_data = response.json()
    assert response_data["detail"] == "Incorrect username or password"


@pytest.mark.asyncio
async def test_refresh_token(client: TestClient) -> None:
    username = get_random_name()
    password = "TestPassword123123"

    data = {"username": username, "password": password, "name": "Test User"}
    response = client.post("/api/v1/auth/register", json=data)
    assert response.status_code == 201

    response = client.post("/api/v1/auth/token", data={"username": username, "password": password})
    refresh_token = response.cookies["refresh_token"]

    response = client.post("/api/v1/auth/refresh-token", cookies={"refresh_token": refresh_token})
    response_data = response.json()
    assert "access_token" in response_data
    assert response_data["access_token"]
    assert "refresh_token" not in response_data
    assert response.cookies["refresh_token"]


@pytest.mark.asyncio
async def test_refresh_token_with_invalid_refresh_token(client: TestClient) -> None:
    response = client.post("/api/v1/auth/refresh-token", cookies={"refresh_token": "invalid_refresh_token"})
    assert response.status_code == 400
    response_data = response.json()
    assert response_data["detail"] == "Could not validate credentials"
