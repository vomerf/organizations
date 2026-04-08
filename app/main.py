from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.routers import organization_router
# from app.deps import get_token_header


app = FastAPI()
# app = FastAPI(dependencies=[Depends(get_token_header)])

app.include_router(organization_router)

Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=["/metrics", "/docs", "/openapi.json", "/redoc"],
).instrument(app).expose(
    app,
    include_in_schema=False,
    endpoint="/metrics",
)
