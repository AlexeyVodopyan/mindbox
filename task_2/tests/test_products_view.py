import pytest
from httpx import AsyncClient

from utils.data_factories import ProductFactory, CategoryFactory, ProductCategoryFactory
from main import app


@pytest.mark.asyncio
async def test_products_view_only_products():
    """
    Teст эндпоинта /products/

    Заполнены только продукты
    """
    products = ProductFactory.create_batch(5)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/products/")

    assert response.status_code == 200
    response_json = response.json()

    assert response_json
    assert len(response_json) == len(products)

    for product in response_json:
        assert product["categories"] == [None]


@pytest.mark.asyncio
async def test_products_view_full_db():
    """
    Teст эндпоинта /products/

    Заполнены все таблицы
    """
    products = ProductFactory.create_batch(5)
    categories = CategoryFactory.create_batch(4)

    categories_products = []

    for product, category in zip(products, categories):
        categories_products.append(ProductCategoryFactory(
            category=category, category_id=category.id,
            product=product, product_id=product.id
        ))

    # Вторая категория для 1 продукта
    categories_products.append(
        ProductCategoryFactory(
            category=categories[-1], category_id=categories[-1].id,
            product=products[0], product_id=products[0].id
        )
    )

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/products/")

    assert response.status_code == 200
    response_json = response.json()

    assert response_json
    assert len(response_json) == len(products)

    # Должны вернуться: 3 продукта с 1 категорией, 1 с двумя и один без
    assert response_json[0]["categories"] == [categories[0].name, categories[-1].name]
    assert response_json[4]["categories"] == [None]

    for i in range(1, 4):
        assert response_json[i]["categories"] == [categories[i].name]


@pytest.mark.asyncio
async def test_products_view_empty_db():
    """
    Teст эндпоинта /products/

    Пустые таблицы
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/products/")

    assert response.status_code == 200
    response_json = response.json()

    assert isinstance(response_json, list)
    assert not response_json
