import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


from app.config.database import get_session
from app.config.settings import settings
from app.models import Building, Organization, OrganizationPhone
from app.repositories.organization import OrganizationRepo
from app.schemas.organization import OrganizationActivityOut, OrganizationOut

router = APIRouter(tags=['Organization'])


@router.get("/organizations/by_building/{building_id}", response_model=list[OrganizationOut])
async def get_organizations_by_building(building_id: int, session: AsyncSession = Depends(get_session)):
    repo = OrganizationRepo(session)
    orgs = await repo.get_data_by_build_id(building_id)

    if not orgs:
        raise HTTPException(status_code=404, detail="В здании нету организаций")

    return [
        OrganizationOut(name=org_name, phones=org_phones) 
        for org_name, org_phones in orgs
    ]


@router.get(
        "/activities/{activity_id}/organizations",
        response_model=list[OrganizationOut]
    )
async def organizations_by_activity(
    activity_id: int,
    session: AsyncSession = Depends(get_session)
):
    repo = OrganizationRepo(session)
    orgs = await repo.get_data_by_activity_id(activity_id)

    if not orgs:
        raise HTTPException(status_code=404, detail="Для данной деятельности не нашлось ни одной организации")

    return [
        OrganizationOut(name=org_name, phones=org_phones) 
        for org_name, org_phones in orgs
    ]

@router.get("/organizations_by_nested_activity", response_model=list[OrganizationActivityOut])
async def get_organizations_by_nested_activity(activity_id: int, session: AsyncSession = Depends(get_session)):
    repo = OrganizationRepo(session)
    orgs = await repo.organizations_by_nested_activity(activity_id)
    return [
        OrganizationActivityOut(
            organization=row["organization_name"],
            activity=row["activity_name"],
            phones=row.get('phone', None)
        )
        for row in orgs
    ]


@router.get("/organization/{organization_id}", response_model=OrganizationOut)
async def get_organization_by_id(
    organization_id: int,
    session: AsyncSession = Depends(get_session)
):
    repo = OrganizationRepo(session)
    org = await repo.get_organization_by_id(organization_id)
    
    if not org:
        raise HTTPException(status_code=404, detail="Организация не найдена")

    return OrganizationOut(name=org['name'], phones=org['phones'])


@router.get("/organization_by_name", response_model=OrganizationOut)
async def get_organization_by_name(
    organization_name: str = Query(..., description="Название организации"),
    session: AsyncSession = Depends(get_session)
):
    repo = OrganizationRepo(session)
    org = await repo.get_organization_by_name(organization_name)
    
    if not org:
        raise HTTPException(status_code=404, detail="Организация не найдена")

    return OrganizationOut(name=org['name'], phones=org['phones']) 


@router.get("/organizations/nearby", response_model=list[OrganizationOut])
async def get_organizations_nearby(
    lat: float = Query(..., description="Широта центра поиска"),
    lon: float = Query(..., description="Долгота центра поиска"),
    radius_m: float = Query(settings.DEFAULT_RADIUS, gt=0, description="Радиус поиска в метрах"),
    session: AsyncSession = Depends(get_session)
):

    point = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)
    point_geog = func.geography(point)

    building_point_geog = func.geography(
        func.ST_SetSRID(func.ST_MakePoint(Building.longitude, Building.latitude), 4326)
    )
    repo = OrganizationRepo(session)
    orgs = await repo.get_organizations_nearby(point_geog, building_point_geog, radius_m)
    if not orgs:
        raise HTTPException(status_code=404, detail="В радиусе {radius_m}м нет ни одной организации")
    
    return [OrganizationOut(name=name, phones=phones) for name, phones in orgs]

