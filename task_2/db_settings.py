import os
from asyncio import current_task

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session

Base = declarative_base()

USER = os.environ.get("POSTGRES_USER")
DB_NAME = os.environ.get("POSTGRES_DB")
HOST = os.environ.get("POSTGRES_HOST")
PORT = os.environ.get("POSTGRES_PORT")
PASS = os.environ.get("POSTGRES_PASSWORD")

SQLALCHEMY_URL = f"postgresql+asyncpg://{USER}:{PASS}@{HOST}:{PORT}/{DB_NAME}"
engine = create_async_engine(SQLALCHEMY_URL)

Session = async_scoped_session(sessionmaker(bind=engine, class_=AsyncSession), scopefunc=current_task)


async def get_session():
    session = Session()
    try:
        yield session
    finally:
        await session.close()
