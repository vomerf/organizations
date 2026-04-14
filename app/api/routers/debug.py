from fastapi import APIRouter, HTTPException

from asyncio import sleep


router = APIRouter(tags=['Debug'])


@router.get("/debug/slow")
async def debug_slow():
    await sleep(1)
    return {"status": "ok"}


@router.get("/debug/error")
async def debug_error():
    raise HTTPException(status_code=500, detail="Test 500 error")
