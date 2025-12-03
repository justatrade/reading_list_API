from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel

from src.database.models import Items, KindEnum, PriorityEnum, StatusEnum
from src.schemas.tags import TagOut


class ItemCreate(BaseModel):
    title: str
    kind: KindEnum
    status: StatusEnum = StatusEnum.planned
    priority: PriorityEnum = PriorityEnum.normal
    notes: Optional[str] = None
    tag_ids: Optional[List[int]] = None


class ItemUpdate(BaseModel):
    title: Optional[str] = None
    kind: Optional[KindEnum] = None
    status: Optional[StatusEnum] = None
    priority: Optional[PriorityEnum] = None
    notes: Optional[str] = None
    tag_ids: Optional[List[int]] = None


class ItemOut(BaseModel):
    id: int
    title: str
    kind: KindEnum
    status: StatusEnum
    priority: PriorityEnum
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    tags: List[TagOut]

    class Config:
        from_attributes = True


ItemSortFields = Enum(
    "ItemSortFields",
    {col.key: col.key for col in Items.__table__.columns},
)
