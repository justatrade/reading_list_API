import enum
import re
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import mapped_column, relationship, Mapped


@as_declarative()
class BaseModel:
    __abstract__ = True
    metadata: MetaData

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    @declared_attr
    def __tablename__(cls):
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class KindEnum(str, enum.Enum):
    book = "book"
    article = "article"


class StatusEnum(str, enum.Enum):
    planned = "planned"
    reading = "reading"
    done = "done"


class PriorityEnum(str, enum.Enum):
    low = "low"
    normal = "normal"
    high = "high"


item_tag = Table(
    "item_tag",
    BaseModel.metadata,
    Column(
        "item_id",
        ForeignKey(column="items.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        ForeignKey(column="tags.id", ondelete="CASCADE"),
        primary_key=True),
)


class Users(BaseModel):
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    display_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    items: Mapped[List["Items"]] = relationship(
        "Items", back_populates="users", cascade="all, delete-orphan"
    )
    #
    # def __repr__(self):
    #     return self.display_name


class Tags(BaseModel):
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)

    users = relationship("Users", backref="tags")
    items = relationship("Items", secondary=item_tag, back_populates="tags")
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="unique_user_tags"),
    )
    #
    # def __repr__(self):
    #     return self.name


class Items(BaseModel):
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    kind: Mapped[KindEnum] = mapped_column(Enum(KindEnum), nullable=False)
    status: Mapped[StatusEnum] = mapped_column(
        Enum(StatusEnum), nullable=False, default=StatusEnum.planned
    )
    priority: Mapped[PriorityEnum] = mapped_column(
        Enum(PriorityEnum), nullable=False, default=PriorityEnum.normal
    )
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), onupdate=datetime.now(timezone.utc)
    )

    users: Mapped["Users"] = relationship("Users", back_populates="items")
    tags: Mapped[List["Tags"]] = relationship(
        "Tags", secondary=item_tag, back_populates="items"
    )
    #
    # def __repr__(self):
    #     return self.title
