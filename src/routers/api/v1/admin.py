from fastapi import APIRouter, HTTPException
import os

from src.database.seed import run_seed


router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/seed")
async def admin_seed():
    result = await run_seed()

    if not result:
        return {"status": "skipped", "message": "Data already exists"}

    return {"status": "ok", "message": "Seed completed"}
