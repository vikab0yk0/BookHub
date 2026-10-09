from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

if TYPE_CHECKING:
    from src.models.role import Role
    from src.models.book import Book
    from src.models.review import Review
    from src.models.user_book import UserBook
    from src.models.bookmark import Bookmark
    from src.models.quote import Quote

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.role_id", ondelete="RESTRICT"), nullable=False, index=True)

    role: Mapped["Role"] = relationship(back_populates="users")
    books_created: Mapped[List["Book"]] = relationship(back_populates="creator")
    reviews: Mapped[List["Review"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    user_books: Mapped[List["UserBook"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    bookmarks: Mapped[List["Bookmark"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    quotes: Mapped[List["Quote"]] = relationship(back_populates="user", cascade="all, delete-orphan")
