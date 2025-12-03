from typing import List, Optional, Sequence
from sqlalchemy import select, update, delete, asc, desc
from sqlalchemy.orm import joinedload

from src.database.repositories.base import BaseRepository
from src.database.models import Items, Tags


class ItemRepository(BaseRepository):

    async def create(self, user_id: int, data) -> Items:
        item = Items(user_id=user_id, **data)
        self.session.add(item)
        await self.session.flush()
        return item

    async def get(self, item_id: int, user_id: int) -> Optional[Items]:
        stmt = (
            select(Items)
            .where(Items.id == item_id, Items.user_id == user_id)
            .options(joinedload(Items.tags))
        )
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def list(
        self,
        user_id: int,
        *,
        status: Optional[str] = None,
        kind: Optional[str] = None,
        priority: Optional[str] = None,
        tags_any: Optional[list[int]] = None,
        title_substring: Optional[str] = None,
        created_from: Optional[str] = None,
        created_to: Optional[str] = None,
        sort_by: str = "created_at",
        sort_dir: str = "desc",
        limit: int = 20,
        offset: int = 0
    ) -> Sequence[Items]:

        stmt = (
            select(Items)
            .where(Items.user_id == user_id)
            .options(joinedload(Items.tags))
        )

        if status:
            stmt = stmt.where(Items.status == status)

        if kind:
            stmt = stmt.where(Items.kind == kind)

        if priority:
            stmt = stmt.where(Items.priority == priority)

        if title_substring:
            stmt = stmt.where(Items.title.ilike(f"%{title_substring}%"))

        if created_from:
            stmt = stmt.where(Items.created_at >= created_from)

        if created_to:
            stmt = stmt.where(Items.created_at <= created_to)

        if tags_any:
            stmt = stmt.join(Items.tags).where(Tags.id.in_(tags_any))

        field = getattr(Items, sort_by)
        stmt = stmt.order_by(desc(field) if sort_dir == "desc" else asc(field))

        stmt = stmt.limit(limit).offset(offset)

        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def update(
            self,
            item_id: int,
            user_id: int,
            data: dict,
            tag_ids: Optional[List[int]] = None,
    ) -> Optional[Items]:
        stmt = (
            update(Items)
            .where(Items.id == item_id, Items.user_id == user_id)
            .values(**data)
            .returning(Items)
        )
        result = await self.session.execute(stmt)
        item = result.scalar_one_or_none()

        if not item:
            return None

        if tag_ids is not None:
            from sqlalchemy import select
            from src.database.models import Tags

            tags_stmt = (
                select(Tags)
                .where(Tags.id.in_(tag_ids), Tags.user_id == user_id)
            )
            tags_result = await self.session.execute(tags_stmt)
            tags = tags_result.scalars().all()
            item.tags = tags

        await self.session.flush()
        await self.session.refresh(item)
        return item

    async def delete(self, item_id: int, user_id: int) -> bool:
        stmt = delete(Items).where(
            Items.id == item_id,
            Items.user_id == user_id
        )
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def update_tags(
            self, item_id: int, user_id: int, tag_ids: List[int]
    ) -> Optional[Items]:
        item = await self.get(item_id, user_id)
        if item is None:
            return None

        stmt = select(Tags).where(
            Tags.user_id == user_id,
            Tags.id.in_(tag_ids)
        )
        result = await self.session.execute(stmt)
        tags = result.scalars().all()

        item.tags = tags
        await self.session.flush()

        return item
