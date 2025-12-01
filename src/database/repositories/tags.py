from sqlalchemy import select
from src.database.models import Tags
from src.database.repositories.base import BaseRepository


class TagRepository(BaseRepository):

    async def get(self, tag_id: int, user_id: int):
        stmt = select(Tags).where(Tags.id == tag_id, Tags.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def create(self, user_id: int, name: str) -> Tags:
        tag = Tags(user_id=user_id, name=name)
        self.session.add(tag)
        await self.session.flush()
        return tag

    async def list(self, user_id: int):
        stmt = select(Tags).where(Tags.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
