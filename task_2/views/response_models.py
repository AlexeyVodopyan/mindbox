from typing import Optional
from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int = Field(title="ID продукта")
    product_name: str = Field(title="Название продукта")
    customer: str = Field(title="Производитель")
    categories: list[Optional[str]] = Field(title="Список категорий")


class Category(BaseModel):
    id: int = Field(title="ID категории")
    category_name: str = Field(title="Название категории")
    products: list[Optional[str]] = Field(title="Список продуктов")


class ProductCategory(BaseModel):
    product_name: Optional[str] = Field(title="Название продукта")
    category_name: Optional[str] = Field(title="Название категории")
