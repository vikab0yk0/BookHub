from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.review import Review
    from src.models.user_book import UserBook
    from src.models.bookmark import Bookmark
    from src.models.quote import Quote


class Book(Base):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    genre: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    annotation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    creator: Mapped[Optional["User"]] = relationship(back_populates="books_created")
    reviews: Mapped[List["Review"]] = relationship(back_populates="book", cascade="all, delete-orphan")
    user_books: Mapped[List["UserBook"]] = relationship(back_populates="book", cascade="all, delete-orphan")
    bookmarks: Mapped[List["Bookmark"]] = relationship(back_populates="book", cascade="all, delete-orphan")
    quotes: Mapped[List["Quote"]] = relationship(back_populates="book", cascade="all, delete-orphan")