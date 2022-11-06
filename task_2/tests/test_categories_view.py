import pytest
from httpx import AsyncClient

from utils.data_factories import ProductFactory, CategoryFactory, ProductCategoryFactory
from main import app


@pytest.mark.asyncio
async def test_categories_view_only_categories():
    """
    Teст эндпоинта /categories/

    Заполнены только продукты
    """
    categories = CategoryFactory.create_batch(5)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/categories/")

    assert response.status_code == 200
    response_json = response.json()

    assert response_json
    assert len(response_json) == len(categories)

    for category in response_json:
        assert category["products"] == [None]


@pytest.mark.asyncio
async def test_categories_view_full_db():
    """
    Teст эндпоинта /categories/

    Заполнены все таблицы
    """
    categories = CategoryFactory.create_batch(5)
    products = ProductFactory.create_batch(4)

    categories_products = []

    for product, category in zip(products, categories):
        categories_products.append(ProductCategoryFactory(
            category=category, category_id=category.id,
            product=product, product_id=product.id
        ))

    # Вторая категория для 1 продукта
    categories_products.append(
        ProductCategoryFactory(
            category=categories[0], category_id=categories[0].id,
            product=products[-1], product_id=products[-1].id
        )
    )

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/categories/")

    assert response.status_code == 200
    response_json = response.json()

    assert response_json
    assert len(response_json) == len(categories)

    # Должны вернуться: 3 категории с 1 продуктом, 1 с двумя и один без
    assert response_json[0]["products"] == [products[0].name, products[-1].name]
    assert response_json[4]["products"] == [None]

    for i in range(1, 4):
        assert response_json[i]["products"] == [products[i].name]


@pytest.mark.asyncio
async def test_categories_view_empty_db():
    """
    Teст эндпоинта /categories/

    Пустые таблицы
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/categories/")

    assert response.status_code == 200
    response_json = response.json()

    assert isinstance(response_json, list)
    assert not response_json
