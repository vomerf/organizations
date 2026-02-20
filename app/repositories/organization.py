from sqlalchemy import func, select, text

from app.models import Activity, Organization, OrganizationPhone, Building
from app.repositories.base import BaseRepo
from app.config.settings import settings

class OrganizationRepo(BaseRepo[Organization]):
    model_class = Organization


    async def get_organization_by_id(self, org_id: int):
        result = await self.session.execute(
            select(
                self.model_class.name.label('name'),
                func.array_agg(OrganizationPhone.phone).label('phones')
            )
            .join(self.model_class.phones)
            .where(self.model_class.id == org_id)
            .group_by(self.model_class.id, self.model_class.name)
        )
        return result.mappings().one_or_none()

    async def get_organization_by_name(self, name: str):
        result = await self.session.execute(
            select(
                self.model_class.name.label('name'),
                func.array_agg(OrganizationPhone.phone).label('phones')
            )
            .join(self.model_class.phones)
            .where(self.model_class.name == name)
            .group_by(self.model_class.id, self.model_class.name)
        )
        return result.mappings().one_or_none()

    async def get_data_by_build_id(self, building_id: int):
        result = await self.session.execute(
            select(
                self.model_class.name.label('name'),
                func.array_agg(OrganizationPhone.phone).label('phones')
            )
            .join(self.model_class.phones)
            .where(self.model_class.building_id == building_id)
            .group_by(self.model_class.id, self.model_class.name)
        )
        return result.all()
    
    async def get_data_by_activity_id(self, activity_id: int):
        result = await self.session.execute(
            select(
                self.model_class.name,
                func.array_agg(OrganizationPhone.phone).label("phones") 
            )
            .join(self.model_class.activities)
            .join(self.model_class.phones)
            .where(Activity.id == activity_id)
            .group_by(self.model_class.id, self.model_class.name)
        )

        return result.all()
    
    async def organizations_by_nested_activity(self, activity_id):
        activity_cte = (
            select(Activity.id)
            .where(Activity.id == activity_id)
            .cte(recursive=True)
        )

        activity_alias = Activity.__table__.alias()
        activity_cte = activity_cte.union_all(
            select(activity_alias.c.id)
            .where(activity_alias.c.parent_id == activity_cte.c.id)
        )

        stmt = (
            select(
                self.model_class.name.label('organization_name'),
                Activity.name.label('activity_name'),
                func.array_agg(OrganizationPhone.phone).label("phone"),
            )
            .join(self.model_class.activities)
            .join(self.model_class.phones)
            .where(Activity.id.in_(select(activity_cte.c.id)))
            .group_by(self.model_class.id, self.model_class.name, Activity.name)
        )

        result = await self.session.execute(stmt)
        return result.mappings().all()


    async def get_organizations_nearby(
        self,
        point_geog,
        building_point_geog,
        radius_m=settings.DEFAULT_RADIUS
    ):
        result = await self.session.execute(
                select(
                    Organization.name.label("name"),
                    func.array_agg(OrganizationPhone.phone).label("phones"),
                )
                .join(Organization.building)
                .join(Organization.phones)
                .where(
                    Building.latitude.is_not(None),
                    Building.longitude.is_not(None),
                    func.ST_DWithin(building_point_geog, point_geog, radius_m),
                )
                .group_by(Organization.id, Organization.name)
            )
        await self.session.execute(text('select 10'))
        return result.all()