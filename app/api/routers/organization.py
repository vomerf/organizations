import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config.database import get_session
from app.models import Activity, Building, Organization, OrganizationPhone
from app.schemas.organization import OrganizationActivityOut, OrganizationOut

router = APIRouter(tags=['Organization'])

# Вынести запросы к БД в отдельный слой!!!

@router.get("/organizations/by_building/{building_id}", response_model=list[OrganizationOut])
async def get_organizations_by_building(building_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(
            Organization.name.label('name'),
            func.array_agg(OrganizationPhone.phone).label('phones')
        )
        .join(Organization.phones)
        .where(Organization.building_id == building_id)
        .group_by(Organization.id, Organization.name)
    )
    organizations = result.all()

    if not organizations:
        raise HTTPException(status_code=404, detail="В здании нету организаций")

    return [
        OrganizationOut(name=org_name, phones=org_phones) 
        for org_name, org_phones in organizations
    ]


@router.get(
        "/activities/{activity_id}/organizations",
        response_model=list[OrganizationOut]
    )
async def organizations_by_activity(
    activity_id: int,
    session: AsyncSession = Depends(get_session)
):
    # летит два запроса в БД
    result = await session.execute(
        select(
            Organization.name,
            func.array_agg(OrganizationPhone.phone).label("phones") 
        )
        .join(Organization.activities)
        .join(Organization.phones) 
        .where(Activity.id == activity_id)
        .group_by(Organization.id, Organization.name)
    )

    result = result.all()

    if not result:
        raise HTTPException(status_code=404, detail="Для данной деятельности не нашлось ни одной организации")

    return [
        OrganizationOut(name=org_name, phones=org_phones) 
        for org_name, org_phones in result
    ]

@router.get("/organizations_by_nested_activity", response_model=list[OrganizationActivityOut])
async def get_organizations_by_nested_activity(activity_id: int, session: AsyncSession = Depends(get_session)):
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

    query = (
        select(
            Organization.name.label('organization_name'),
            Activity.name.label('activity_name'),
            func.array_agg(OrganizationPhone.phone).label("phone"),
        )
        .join(Organization.activities)
        .join(Organization.phones)
        .where(Activity.id.in_(select(activity_cte.c.id)))
        .group_by(Organization.id, Organization.name, Activity.name)
    )

    result = await session.execute(query)
    rows = result.mappings().all()

    return [
        OrganizationActivityOut(
            organization=row["organization_name"],
            activity=row["activity_name"],
            phones=row.get('phone', None)
        )
        for row in rows
    ]


@router.get("/organization/{organization_id}", response_model=OrganizationOut)
async def get_organization_by_id(
    organization_id: int,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(
            Organization.name.label('name'),
            func.array_agg(OrganizationPhone.phone).label('phones')
        )
        .join(Organization.phones)
        .where(Organization.id == organization_id)
        .group_by(Organization.id, Organization.name)
    )
    org = result.all()[0]
    
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    return OrganizationOut(name=org[0], phones=org[1])


@router.get("/organization_by_name", response_model=list[OrganizationOut])
async def get_organization_by_name(
    organization_name: str,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(
            Organization.name.label('name'),
            func.array_agg(OrganizationPhone.phone).label('phones')
        )
        .join(Organization.phones)
        .where(Organization.name == organization_name)
        .group_by(Organization.id, Organization.name)
    )

    result = result.all()
    
    if not result:
        raise HTTPException(status_code=404, detail="Организация не найдена")

    return [
        OrganizationOut(name=org_name, phones=org_phones) 
        for org_name, org_phones in result
    ]



@router.get("/organizations/nearby", response_model=list[OrganizationOut])
async def get_organizations_nearby(
    lat: float = Query(..., description="Широта центра поиска"),
    lon: float = Query(..., description="Долгота центра поиска"),
    radius_km: float = Query(5.0, description="Радиус поиска в километрах"),
    session: AsyncSession = Depends(get_session)
):
    """
    Получить список организаций в заданном радиусе (km) от точки (lat, lon).
    
    Для больших данных рекомендуется использовать PostGIS и гео-индексы,
    тогда поиск будет гораздо быстрее и точнее.
    """
    # Перевод центра в радианы
    lat0_rad = math.radians(lat)
    lon0_rad = math.radians(lon)
    R = 6371  # радиус Земли в км

    # SQLAlchemy выражение Хаверсина
    distance_expr = (
        R * 2 * func.asin(
            func.sqrt(
                func.pow(func.sin((func.radians(Building.latitude) - lat0_rad) / 2), 2) +
                func.cos(lat0_rad) *
                func.cos(func.radians(Building.latitude)) *
                func.pow(func.sin((func.radians(Building.longitude) - lon0_rad) / 2), 2)
            )
        )
    )

    result = await session.execute(
        select(Building).options(selectinload(Building.organizations)).where(distance_expr <= radius_km)
    )
    buildings = result.scalars().all()

    organizations = []
    for building in buildings:
        organizations.extend(building.organizations)

    return organizations
