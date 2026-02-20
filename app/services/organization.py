import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


from app.config.database import get_session
from app.config.settings import settings
from app.models import Building, Organization, OrganizationPhone
from app.repositories.organization import OrganizationRepo
from app.schemas.organization import OrganizationActivityOut, OrganizationOut


class OrganizationService:

    async def get_organizations_nearby(
        self,
        session: AsyncSession,
        lat: float,
        lon: float,
        radius_m: float
    ):
        point = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)
        point_geog = func.geography(point)

        building_point_geog = func.geography(
            func.ST_SetSRID(func.ST_MakePoint(Building.longitude, Building.latitude), 4326)
        )
        repo = OrganizationRepo(session)
        orgs = await repo.get_organizations_nearby_db(point_geog, building_point_geog, radius_m)
        return orgs
    
    async def get_organizations_by_building(self, session: AsyncSession, building_id: int):
        repo = OrganizationRepo(session)
        orgs = await repo.get_data_by_build_id_db(building_id)
        return orgs
    

    async def get_organizations_by_activity(
        self,
        session: AsyncSession,
        activity_id: int
    ):
        repo = OrganizationRepo(session)
        orgs = await repo.get_data_by_activity_id_db(activity_id)
        return orgs
    
    async def get_organizations_by_nested_activity(
        self,
        session: AsyncSession,
        activity_id: int
    ):
        repo = OrganizationRepo(session)
        orgs = await repo.organizations_by_nested_activity_db(activity_id)
        return orgs
    

    async def get_organization_by_id(\
        self,
        session: AsyncSession,
        organization_id: int
    ):
        repo = OrganizationRepo(session)
        org = await repo.get_organization_by_id_db(organization_id)
        return org
    
    async def get_organization_by_name(
        self,
        session: AsyncSession,
        organization_name: str
    ):
        repo = OrganizationRepo(session)
        org = await repo.get_organization_by_name_db(organization_name)
        return org