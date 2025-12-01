from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.dependencies import get_db_session
from src.database.repositories import TagRepository
from src.schemas.tags import TagCreate, TagOut

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("/", response_model=TagOut)
async def create_tag(
    payload: TagCreate,
    session: AsyncSession = Depends(get_db_session),
    user_id: int = 1,
):
    repo = TagRepository(session)
    return await repo.create(user_id, payload.name)


@router.get("/", response_model=list[TagOut])
async def list_tags(
    session: AsyncSession = Depends(get_db_session),
    user_id: int = 1,
):
    repo = TagRepository(session)
    return await repo.list(user_id)
