from datetime import datetime
from uuid import UUID

from sqlalchemy import ARRAY, Date, String, Text
from sqlalchemy import UUID as UUID_alchemy  # noqa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "posts"
    id: Mapped[UUID] = mapped_column(
        UUID_alchemy(as_uuid=True),
        primary_key=True,
    )
    rubrics: Mapped[list[str]] = mapped_column(ARRAY(String))
    text: Mapped[str] = mapped_column(Text)
    created_date: Mapped[datetime] = mapped_column(Date, default=datetime.now())
