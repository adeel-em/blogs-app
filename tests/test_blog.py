import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_blog(client: AsyncClient, access_token):
    blog_data = {"title": "Test Blog", "content": "This is a test blog content."}
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.post("/api/v1/blogs/", json=blog_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == blog_data["title"]


@pytest.mark.asyncio
async def test_get_blogs(client: AsyncClient):
    response = await client.get("/api/v1/blogs/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
