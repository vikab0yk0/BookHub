from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, DateTime, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.book import Book

class UserBook(Base):
    __tablename__ = "user_books"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.book_id", ondelete="CASCADE"), primary_key=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    added_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("status IN ('favorite', 'read', 'planned')", name="check_user_book_status"),
    )

    user: Mapped["User"] = relationship(back_populates="user_books")
    book: Mapped["Book"] = relationship(back_populates="user_books")
