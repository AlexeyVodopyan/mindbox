import pytest_asyncio
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from mock import MagicMock

from utils.data_factories import CategoryFactory, ProductFactory, ProductCategoryFactory
from db_settings import engine


@pytest_asyncio.fixture
async def mock_session():

    connection = await engine.connect()
    trans = await connection.begin()

    Session = sessionmaker(connection, expire_on_commit=False, class_=AsyncSession)
    session = Session()

    async def mock_delete(instance):
        session.expunge(instance)
        return await asyncio.sleep(0)

    session.commit = MagicMock(side_effect=session.flush)
    session.delete = MagicMock(side_effect=mock_delete)

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()
        await engine.dispose()


@pytest_asyncio.fixture(autouse=True)
def setup_factories(mock_session: AsyncSession) -> None:
    CategoryFactory.session = mock_session
    ProductFactory.session = mock_session
    ProductCategoryFactory.session = mock_session

