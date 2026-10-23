from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.quote import Quote


class QuoteRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user_id: int, book_id: int,
               quote_text: str, page: int = None) -> Quote:
        quote = Quote(
            user_id=user_id,
            book_id=book_id,
            quote_text=quote_text,
            page=page,
        )
        self.session.add(quote)
        self.session.commit()
        self.session.refresh(quote)
        return quote

    def list_by_user(self, user_id: int) -> List[Quote]:
        stmt = select(Quote).where(Quote.user_id == user_id)
        return list(self.session.scalars(stmt).all())

    def delete(self, quote_id: int) -> bool:
        quote = self.session.get(Quote, quote_id)
        if not quote:
            return False
        self.session.delete(quote)
        self.session.commit()
        return True