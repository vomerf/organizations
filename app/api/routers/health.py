from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from app.config.database import engine

router = APIRouter(tags=['Health'])


@router.get("/health/live", include_in_schema=False)
async def health_live():
    return {"status": "ok"}


@router.get("/health/ready", include_in_schema=False)
async def health_ready():
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "status_unavailable"},
        )
