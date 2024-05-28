import pytest
from httpx import AsyncClient
from app.schemas.user import UserCreate, UserInDB
from app.core.security import create_access_token


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    user_data = {"email": "test@example.com", "password": "password123"}
    response = await client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient):
    response = await client.get("/api/v1/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
