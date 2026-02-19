from typing import Generic, Type, TypeVar, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepo(Generic[ModelType]):
    model_class: Type[ModelType]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_data_by_id(self, obj_id: int):
        stmt = select(self.model_class).where(self.model_class.id == obj_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self):
        stmt = select(self.model_class)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_data_by_params(self, **params: Any):
        stmt = select(self.model_class)

        for field, value in params.items():
            if not hasattr(self.model_class, field):
                raise ValueError(f"{field} is not a valid column")

            column = getattr(self.model_class, field)
            stmt = stmt.where(column == value)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, **data: Any):
        obj = self.model_class(**data)
        self.session.add(obj)
        await self.session.flush()
        return obj
    
    async def delete(self, obj):
        await self.session.delete(obj)
        await self.session.flush()
        return obj