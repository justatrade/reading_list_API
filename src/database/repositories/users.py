from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Users
from src.schemas.users import UserCreate, UserUpdate


class UserRepository:
    @staticmethod
    async def get_by_id(session: AsyncSession, user_id: int) -> Users | None:
        result = await session.execute(select(Users).where(Users.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(session: AsyncSession) -> list[Users]:
        result = await session.execute(select(Users))
        return list(result.scalars().all())
    
    @staticmethod
    async def create(session: AsyncSession, data: UserCreate) -> Users:
        user: Users = Users(
            email=data.email,
            display_name=data.display_name,
            created_at=datetime.now(),
        )
        session.add(user)
        await session.flush()
        return user

    @staticmethod
    async def update(session: AsyncSession, user: Users, data: UserUpdate) -> Users:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        await session.flush()
        await session.refresh(user)
        return user

    @staticmethod
    async def delete(session: AsyncSession, user: Users) -> None:
        await session.delete(user)
