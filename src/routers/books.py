from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.dependencies.auth import require_admin
from src.dependencies.db import get_session
from src.models.user import User
from src.repositories.book_repository import BookRepository
from src.schemas.book import BookCreate, BookFull, BookShort, BookUpdate


router = APIRouter(prefix="/books", tags=["books"])


@router.get("", response_model=list[BookShort])
def list_books(
    genre: str | None = None,
    author: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session),
):
    """Список книг с фильтрацией и пагинацией."""
    return BookRepository(session).get_all(
        genre=genre,
        author=author,
        skip=skip,
        limit=limit,
    )


@router.get("/{book_id}", response_model=BookFull)
def get_book(
    book_id: int,
    session: Session = Depends(get_session),
):
    """Карточка книги по ID."""
    book = BookRepository(session).get_by_id(book_id)
    if not book:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Книга не найдена")
    return book


@router.post("", response_model=BookFull, status_code=status.HTTP_201_CREATED)
def create_book(
    data: BookCreate,
    admin: User = Depends(require_admin),
    session: Session = Depends(get_session),
):
    """Создать книгу. Только admin."""
    return BookRepository(session).create(
        title=data.title,
        author=data.author,
        genre=data.genre,
        annotation=data.annotation,
        content=data.content,
        created_by=admin.user_id,
    )


@router.put("/{book_id}", response_model=BookFull)
def update_book(
    book_id: int,
    data: BookUpdate,
    admin: User = Depends(require_admin),
    session: Session = Depends(get_session),
):
    repo = BookRepository(session)
    book = repo.get_by_id(book_id)
    if not book:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Книга не найдена")
    return repo.update(book_id, **data.model_dump(exclude_unset=True))


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    admin: User = Depends(require_admin),
    session: Session = Depends(get_session),
):
    repo = BookRepository(session)
    if not repo.delete(book_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Книга не найдена")