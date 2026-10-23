from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.dependencies.auth import get_current_user
from src.dependencies.db import get_session
from src.models.user import User
from src.repositories.book_repository import BookRepository
from src.repositories.review_repository import ReviewRepository
from src.schemas.review import ReviewCreate, ReviewOut


router = APIRouter(tags=["reviews"])


@router.get("/books/{book_id}/reviews", response_model=list[ReviewOut])
def list_reviews(book_id: int, session: Session = Depends(get_session)):
    if not BookRepository(session).get_by_id(book_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Книга не найдена")
    return ReviewRepository(session).list_by_book(book_id)


@router.post("/books/{book_id}/reviews", response_model=ReviewOut, status_code=201)
def create_review(
    book_id: int,
    data: ReviewCreate,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
   
    if not BookRepository(session).get_by_id(book_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Книга не найдена")
    return ReviewRepository(session).create(
        user_id=user.user_id,
        book_id=book_id,
        rating=data.rating,
        comment=data.comment,
    )


@router.delete("/reviews/{review_id}", status_code=204)
def delete_review(
    review_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):

    repo = ReviewRepository(session)
    review = repo.get_by_id(review_id)
    if not review:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Отзыв не найден")
    if review.user_id != user.user_id and user.role.name != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Нельзя удалить чужой отзыв")
    repo.delete(review_id)