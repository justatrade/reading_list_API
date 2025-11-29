import enum
import re
from datetime import datetime
from typing import Optional

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
    name="item_tag",
    metadata=BaseModel.metadata,
    args=[
        Column(
            __name_pos="item_id",
            args=[ForeignKey(column="items.id", ondelete="CASCADE")],
            primary_key=True,
        ),
        Column(
            __name_pos="tag_id",
            args=[ForeignKey(column="tags.id", ondelete="CASCADE")],
            primary_key=True),
    ],
)


class User(BaseModel):
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    display_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=datetime.now()
    )

    items = relationship(
        "Item", back_populates="user", cascade="all, delete-orphan"
    )


class Tag(BaseModel):
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)

    user = relationship("User", backref="tags")
    items = relationship("Item", secondary=item_tag, back_populates="tags")


class Item(BaseModel):
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    kind = Column(Enum(KindEnum), nullable=False)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.planned)
    priority = Column(Enum(PriorityEnum), nullable=False, default=PriorityEnum.normal)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, onupdate=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())

    user = relationship("User", back_populates="items")
    tags = relationship("Tag", secondary=item_tag, back_populates="items")