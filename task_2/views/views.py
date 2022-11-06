from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db_settings import get_session
from utils.queries import get_products, get_categories, get_product_category_pairs
from views.response_models import Category, Product, ProductCategory

main_router = APIRouter(
    tags=["Data API"]
)


@main_router.get("/products/", response_model=list[Product])
async def products_list(session: AsyncSession = Depends(get_session)) -> list[Product]:
    """
    Эндпоинт для получения списка продуктов с категориями

    :param session: сессия БД
    :return: список продуктов с категориями
    """
    return await get_products(session)


@main_router.get("/categories/", response_model=list[Category])
async def categories_list(session: AsyncSession = Depends(get_session)) -> list[Category]:
    """
    Эндпоинт для получения списка категорий с продуктами

    :param session: сессия БД
    :return: список категорий с продуктами
    """
    return await get_categories(session)


@main_router.get("/product-category-pairs/", response_model=list[ProductCategory])
async def product_category_pairs(session: AsyncSession = Depends(get_session)) -> list[ProductCategory]:
    """
    Эндпоинт для получения списка "Имя продукта - Имя категории"

    :param session: сессия БД
    :return: список "Имя продукта - Имя категории"
    """
    return await get_product_category_pairs(session)
