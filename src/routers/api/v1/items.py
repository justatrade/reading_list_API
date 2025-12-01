from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.dependencies import get_db_session
from src.database.repositories import ItemRepository
from src.schemas.items import ItemCreate, ItemOut, ItemSortFields, ItemUpdate
from src.database.models import StatusEnum, KindEnum, PriorityEnum

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("/", response_model=ItemOut)
async def create_item(
    payload: ItemCreate,
    session: AsyncSession = Depends(get_db_session),
    user_id: int = Query(...),
):
    repo = ItemRepository(session)
    item = await repo.create(user_id, payload.model_dump(exclude_unset=True))
    return item


@router.get("/{item_id}", response_model=ItemOut)
async def get_item(
    item_id: int,
    session: AsyncSession = Depends(get_db_session),
    user_id: int = Query(...),
):
    repo = ItemRepository(session)
    item = await repo.get(item_id, user_id)
    if not item:
        raise HTTPException(404, "Item not found")
    return item


# List with filters
@router.get("/", response_model=list[ItemOut])
async def list_items(
    session: AsyncSession = Depends(get_db_session),
    user_id: int = Query(...),
    status: StatusEnum | None = None,
    kind: KindEnum | None = None,
    priority: PriorityEnum | None = None,
    tags: list[int] | None = Query(None),
    title: str | None = None,
    limit: int = 50,
    offset: int = 0,
    order_by: ItemSortFields = ItemSortFields.created_at,
    direction: str = "desc",
):
    repo = ItemRepository(session)
    items = await repo.list(
        user_id=user_id,
        status=status,
        kind=kind,
        priority=priority,
        tags_any=tags,
        title_substring=title,
        limit=limit,
        offset=offset,
        sort_by=order_by,
        sort_dir=direction,
    )
    return items


# Update
@router.patch("/{item_id}", response_model=ItemOut)
async def update_item(
    item_id: int,
    payload: ItemUpdate,
    session: AsyncSession = Depends(get_db_session),
    user_id: int = Query(...),
):
    repo = ItemRepository(session)
    item = await repo.get(item_id, user_id)
    if not item:
        raise HTTPException(404, "Item not found")

    item = await repo.update(item, payload.model_dump(exclude_unset=True))
    return item


# Delete
@router.delete("/{item_id}", status_code=204)
async def delete_item(
    item_id: int,
    session: AsyncSession = Depends(get_db_session),
    user_id: int = Query(...),
):
    repo = ItemRepository(session)
    item = await repo.get(item_id, user_id)
    if not item:
        raise HTTPException(404, "Item not found")

    await repo.delete(item.id, user_id)
