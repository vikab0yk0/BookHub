from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.dependencies.auth import get_current_user
from src.dependencies.db import get_session
from src.models.user import User
from src.repositories.book_repository import BookRepository
from src.repositories.user_book_repository import UserBookRepository
from src.schemas.user_book import UserBookIn, UserBookOut


router = APIRouter(tags=["user_books"])


@router.get("/me/lists/{status}", response_model=list[UserBookOut])
def get_my_list(
    status: str,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Мои книги с указанным статусом."""
    return UserBookRepository(session).get_user_books(user.user_id, status)


@router.post("/books/{book_id}/lists", response_model=UserBookOut)
def add_to_list(
    book_id: int,
    data: UserBookIn,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Добавить книгу в список."""
    if not BookRepository(session).get_by_id(book_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Книга не найдена")
    return UserBookRepository(session).add_to_list(
        user_id=user.user_id,
        book_id=book_id,
        status=data.status,
    )


@router.delete("/books/{book_id}/lists", status_code=204)
def remove_from_list(
    book_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Убрать книгу из списков."""
    repo = UserBookRepository(session)
    if not repo.remove(user.user_id, book_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Запись не найдена")