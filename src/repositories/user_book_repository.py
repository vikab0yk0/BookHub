from typing import List
from sqlalchemy import select, inspect
from sqlalchemy.orm import Session, selectinload
from src.models.user_book import UserBook

class UserBookRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_to_list(self, user_id: int, book_id: int, status: str) -> UserBook:
        user_book = UserBook(user_id=user_id, book_id=book_id, status=status)
        self.session.merge(user_book)
        # print(inspect(user_book).transient)
        self.session.commit()
        # print(inspect(user_book).transient)
        return user_book

    def get_user_books(self, user_id: int, status: str = None) -> List[UserBook]:
        stmt = select(UserBook).where(UserBook.user_id == user_id).options(selectinload(UserBook.book))
        if status:
            stmt = stmt.where(UserBook.status == status)
        return list(self.session.scalars(stmt).all())
