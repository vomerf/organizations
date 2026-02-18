from app.repositories.base import BaseRepo
from app.models.organization import Organization
from app.config.database import Base


class OrganizationRepo(BaseRepo):
    model_class: Base = Organization

    async def get_data_by_build_id(self, build_id: int):
        pass


