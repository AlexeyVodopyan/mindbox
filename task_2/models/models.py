from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db_settings import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, comment="Название")
    customer = Column(String, comment="Производитель")
    products_categories = relationship("ProductCategory", back_populates="product")


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, comment="Название")
    products_categories = relationship("ProductCategory", back_populates="category")


class ProductCategory(Base):
    __tablename__ = "product_category"

    id = Column(Integer, primary_key=True, autoincrement=True)

    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product")

    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category")
