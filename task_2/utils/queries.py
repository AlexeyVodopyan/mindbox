from sqlalchemy import select
from sqlalchemy.dialects.postgresql import array_agg
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Product, Category, ProductCategory


async def get_products(session: AsyncSession) -> list:
    """
    Запрос на получение всех продуктов и привязанных к ним категорий

    :param session: сессия БД
    :return: список продуктов с категориями
    """
    query = select(
        Product.id,
        Product.name.label("product_name"),
        Product.customer,
        array_agg(Category.name).label("categories")
    ). \
        join(ProductCategory, Product.id == ProductCategory.product_id, isouter=True). \
        join(Category, ProductCategory.category_id == Category.id, isouter=True). \
        group_by(Product.id, Product.name, Product.customer). \
        order_by(Product.id)

    result = await session.execute(query)
    return result.all()


async def get_categories(session: AsyncSession) -> list:
    """
    Запрос на получение всех категорий с продуктами

    :param session: сессия БД
    :return: список категорий с продуктами
    """

    query = select(
        Category.id,
        Category.name.label("category_name"),
        array_agg(Product.name).label("products")
    ). \
        join(ProductCategory, Category.id == ProductCategory.category_id, isouter=True). \
        join(Product, ProductCategory.product_id == Product.id, isouter=True). \
        group_by(Category.id, Category.name). \
        order_by(Category.id)

    result = await session.execute(query)
    return result.all()


async def get_product_category_pairs(session: AsyncSession) -> list:
    """
    Запрос на получение всех пар «Имя продукта – Имя категории».

    :param session: сессия БД
    :return: список пар "Имя продукта - Имя категории"
    """

    query = select(
        Product.name.label("product_name"),
        Category.name.label("category_name"),
    ). \
        join(ProductCategory, Product.id == ProductCategory.product_id, full=True). \
        join(Category, ProductCategory.category_id == Category.id, full=True)

    result = await session.execute(query)
    return result.all()
