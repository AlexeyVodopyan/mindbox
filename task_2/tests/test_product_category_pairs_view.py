import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_pairs_view_empty_db():
    """
    Teст эндпоинта /product-category-pairs/

    Пустые таблицы
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/product-category-pairs/")

    assert response.status_code == 200
    response_json = response.json()

    assert isinstance(response_json, list)
    assert not response_json
