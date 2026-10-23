from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.models.book import Book
from src.models.review import Review


class BookRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, title: str, author: str, genre: str = None,
               annotation: str = None, content: str = None,
               created_by: int = None) -> Book:
        book = Book(
            title=title, author=author, genre=genre,
            annotation=annotation, content=content, created_by=created_by
        )
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return book

    def get_by_id(self, book_id: int) -> Optional[Book]:
        return self.session.get(Book, book_id)

    def get_with_reviews(self, book_id: int) -> Optional[Book]:
        stmt = (
            select(Book)
            .where(Book.book_id == book_id)
            .options(selectinload(Book.reviews).selectinload(Review.user))
        )
        return self.session.scalar(stmt)

    def get_all(
        self,
        genre: str | None = None,
        author: str | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> List[Book]:
        stmt = select(Book)

        if genre:
            stmt = stmt.where(Book.genre == genre)

        if author:
            stmt = stmt.where(Book.author.ilike(f"%{author}%"))

        stmt = stmt.order_by(Book.book_id).offset(skip).limit(limit)
        return list(self.session.scalars(stmt).all())

    def update(self, book_id: int, **kwargs) -> Optional[Book]:
        book = self.get_by_id(book_id)
        if not book:
            return None
        for key, value in kwargs.items():
            if hasattr(book, key):
                setattr(book, key, value)
        self.session.commit()
        self.session.refresh(book)
        return book

    def delete(self, book_id: int) -> bool:
        book = self.get_by_id(book_id)
        if not book:
            return False
        self.session.delete(book)
        self.session.commit()
        return True