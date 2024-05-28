import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_comment(client: AsyncClient, access_token):
    comment_data = {"content": "This is a test comment.", "blog_id": 1}
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.post(
        "/api/v1/comments/", json=comment_data, headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == comment_data["content"]


@pytest.mark.asyncio
async def test_get_comments(client: AsyncClient):
    response = await client.get("/api/v1/comments/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
