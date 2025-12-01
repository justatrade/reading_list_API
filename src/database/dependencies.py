from src.database.connection import DatabaseConnection
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_session() -> AsyncSession:
    async with DatabaseConnection.get_session() as session:
        yield session
