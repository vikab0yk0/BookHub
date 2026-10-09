from typing import Optional
from sqlalchemy.orm import Session
from src.models.review import Review

class ReviewRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user_id: int, book_id: int, rating: int, comment: str = None) -> Review:
        review = Review(user_id=user_id, book_id=book_id, rating=rating, comment=comment)
        self.session.add(review)
        self.session.commit()
        self.session.refresh(review)
        return review

    def delete(self, review_id: int) -> bool:
        review = self.session.get(Review, review_id)
        if not review:
            return False
        self.session.delete(review)
        self.session.commit()
        return True
