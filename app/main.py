from fastapi import Depends, FastAPI

from app.api.routers import organization_router
from app.deps import get_token_header

# app = FastAPI(dependencies=[Depends(get_token_header)])
app = FastAPI()


app.include_router(organization_router)