
from typing import TYPE_CHECKING

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base

if TYPE_CHECKING:
    from .organization import Organization

class Building(Base):
    __tablename__ = 'building'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city: Mapped[str] = mapped_column(String, nullable=False)
    street: Mapped[str] = mapped_column(String, nullable=False)
    house: Mapped[str] = mapped_column(String, nullable=False)
    office: Mapped[str | None] = mapped_column(String)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    organizations: Mapped[list["Organization"]] = relationship(
        back_populates="building"
    )

    def __str__(self):
        return f'{self.city} - {self.street} - {self.house}'