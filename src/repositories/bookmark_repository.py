from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.bookmark import Bookmark


class BookmarkRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user_id: int, book_id: int,
               position: int, note: str = None) -> Bookmark:
        bookmark = Bookmark(
            user_id=user_id,
            book_id=book_id,
            position=position,
            note=note,
        )
        self.session.add(bookmark)
        self.session.commit()
        self.session.refresh(bookmark)
        return bookmark

    def list_by_user(self, user_id: int) -> List[Bookmark]:
        stmt = select(Bookmark).where(Bookmark.user_id == user_id)
        return list(self.session.scalars(stmt).all())

    def delete(self, bookmark_id: int) -> bool:
        bookmark = self.session.get(Bookmark, bookmark_id)
        if not bookmark:
            return False
        self.session.delete(bookmark)
        self.session.commit()
        return True