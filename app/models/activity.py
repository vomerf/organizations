from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base, engine

if TYPE_CHECKING:
    from .organization import Organization, OrganizationActivity

class Activity(Base):
    __tablename__ = 'activity'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("activity.id"))

    parent: Mapped["Activity"] = relationship(
        remote_side="Activity.id",
        backref="children"
    )

    level: Mapped[int] = mapped_column(nullable=False)
    # Доступ к промежуточной таблице
    organization_activities: Mapped[list["OrganizationActivity"]] = relationship(
        back_populates="activity",
        cascade="all, delete-orphan"
    )

    # Получение всех объектов через промежуточную таблицу, только для чтения
    # внисить изменения лучше через organization_activities
    organizations: Mapped[list["Organization"]] = relationship(
        secondary="organization_activity",
        viewonly=True
    )

    __table_args__ = (
        CheckConstraint("level BETWEEN 1 AND 3", name="activity_level_check"),
    )

    def __str__(self):
        if self.parent_id:
            return f'{self.parent.name} -> {self.name}'
        return self.name


# import asyncio

# async def init_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# if __name__ == "__main__":
#     asyncio.run(init_db())