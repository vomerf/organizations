from typing import Annotated

from fastapi import Header, HTTPException

from app.config.settings import settings


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != settings.TOKEN:
        raise HTTPException(status_code=400, detail="X-Token невалидный")
