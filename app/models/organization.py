
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base

if TYPE_CHECKING:
    from .activity import Activity
    from .building import Building


class Organization(Base):
    __tablename__ = 'organization'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    building_id: Mapped[int] = mapped_column(ForeignKey("building.id"))
    building: Mapped["Building"] = relationship(back_populates="organizations")

    organization_activities: Mapped[list["OrganizationActivity"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan"
    )

    activities: Mapped[list["Activity"]] = relationship(
        secondary="organization_activity",
        viewonly=True
    )
    phones: Mapped[list["OrganizationPhone"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan"
    )

    def __str__(self):
        return f'{self.name}'
    

class OrganizationPhone(Base):
    __tablename__ = "organization_phone"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
    phone: Mapped[str] = mapped_column(String, nullable=False)

    organization: Mapped["Organization"] = relationship(
        back_populates="phones"
    )


class OrganizationActivity(Base):
    __tablename__ = "organization_activity"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organization.id"),
        primary_key=True
    )
    activity_id: Mapped[int] = mapped_column(
        ForeignKey("activity.id"),
        primary_key=True
    )
    organization: Mapped["Organization"] = relationship(
        back_populates="organization_activities"
    )
    activity: Mapped["Activity"] = relationship(
        back_populates="organization_activities"
    )