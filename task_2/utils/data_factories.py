import factory
import asyncio

from \
    db_settings import Session
from models.models import Product, Category, ProductCategory


class CategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Category
        sqlalchemy_session = Session

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("word")


class ProductFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Product
        sqlalchemy_session = Session

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("word")
    customer = factory.Faker("word")


class ProductCategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ProductCategory
        sqlalchemy_session = Session

    id = factory.Sequence(lambda n: n)
    category = factory.SubFactory(CategoryFactory)
    product = factory.SubFactory(ProductFactory)


async def create_fake_data(n_products: int = 50, n_categories: int = 5):
    categories = []
    products = []

    async with Session() as session:

        for _ in range(n_categories):
            categories.append(CategoryFactory())

        for _ in range(n_products):
            products.append(ProductFactory())

        # Часть продуктов будут привязаны к одной категории, часть к нескольким,
        # Часть продуктов не будет привязано, часть категорий не будет привязано
        products_to_one = int(0.8 * n_products)

        for i in range(products_to_one):
            ProductCategoryFactory(product_id=products[i].id, category_id=categories[0].id,
                                   product=products[i], category=categories[0])

        products_to_two = products_to_one // 2

        for i in range(products_to_two):
            ProductCategoryFactory(product_id=products[i].id, category_id=categories[1].id,
                                   product=products[i], category=categories[1])

        product_to_three = products_to_two // 2

        for i in range(product_to_three):
            ProductCategoryFactory(product_id=products[i].id, category_id=categories[2].id,
                                   product=products[i], category=categories[2])

        await session.commit()


if __name__ == "__main__":
    asyncio.run(create_fake_data())
