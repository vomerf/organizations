from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase

from app.config.settings import settings

engine = create_async_engine(
    settings.database_url, echo=True
)

async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def get_session():
    '''Получение сессии в запросе, нужно явно делать commit'''
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
