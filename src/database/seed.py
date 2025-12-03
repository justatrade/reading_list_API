import asyncio
from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from src.database.connection import DatabaseConnection
from src.database.models import (
    Users, Tags, Items,
    KindEnum, StatusEnum, PriorityEnum
)


async def run_seed() -> bool:
    async with DatabaseConnection.get_session() as db:

        exists = await db.execute(select(Users))
        if exists.scalars().first():
            return False

        now = datetime.now(timezone.utc)

        user1 = Users(
            email="alice@example.com",
            display_name="Alice",
            created_at=now,
        )

        user2 = Users(
            email="bob@example.com",
            display_name="Bob",
            created_at=now,
        )

        db.add_all([user1, user2])
        await db.flush()

        # User 1 tags
        t_u1_reading = Tags(user_id=user1.id, name="reading")
        t_u1_fiction = Tags(user_id=user1.id, name="fiction")
        t_u1_science = Tags(user_id=user1.id, name="science")

        # User 2 tags
        t_u2_business = Tags(user_id=user2.id, name="business")
        t_u2_history = Tags(user_id=user2.id, name="history")
        t_u2_tech = Tags(user_id=user2.id, name="tech")

        db.add_all([
            t_u1_reading, t_u1_fiction, t_u1_science,
            t_u2_business, t_u2_history, t_u2_tech
        ])
        await db.flush()

        items = [
            Items(
                user_id=user1.id,
                title="The Martian",
                kind=KindEnum.book,
                status=StatusEnum.reading,
                priority=PriorityEnum.high,
                notes="Great sci-fi novel.",
                created_at=now - timedelta(days=5),
                updated_at=now,
                tags=[t_u1_fiction, t_u1_science]
            ),
            Items(
                user_id=user1.id,
                title="Python Cookbook",
                kind=KindEnum.book,
                status=StatusEnum.planned,
                priority=PriorityEnum.normal,
                notes="Must read for deeper Python knowledge.",
                created_at=now - timedelta(days=2),
                updated_at=now,
                tags=[t_u1_science]
            ),
            Items(
                user_id=user1.id,
                title="Tech News Digest",
                kind=KindEnum.article,
                status=StatusEnum.done,
                priority=PriorityEnum.low,
                notes=None,
                created_at=now - timedelta(days=1),
                updated_at=now,
                tags=[t_u1_reading]
            ),
            Items(
                user_id=user2.id,
                title="Business Strategy 2025",
                kind=KindEnum.article,
                status=StatusEnum.planned,
                priority=PriorityEnum.high,
                notes="Long read.",
                created_at=now - timedelta(days=3),
                updated_at=now,
                tags=[t_u2_business]
            ),
            Items(
                user_id=user2.id,
                title="History of Roman Empire",
                kind=KindEnum.book,
                status=StatusEnum.reading,
                priority=PriorityEnum.normal,
                notes="Very interesting.",
                created_at=now - timedelta(days=7),
                updated_at=now,
                tags=[t_u2_history]
            ),
            Items(
                user_id=user2.id,
                title="AI Trends in 2025",
                kind=KindEnum.article,
                status=StatusEnum.done,
                priority=PriorityEnum.high,
                notes=None,
                created_at=now - timedelta(hours=12),
                updated_at=now,
                tags=[t_u2_tech]
            ),
        ]

        db.add_all(items)

        return True


if __name__ == "__main__":
    asyncio.run(run_seed())
