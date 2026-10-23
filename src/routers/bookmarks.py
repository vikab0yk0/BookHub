from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.dependencies.auth import get_current_user
from src.dependencies.db import get_session
from src.models.user import User
from src.repositories.book_repository import BookRepository
from src.repositories.bookmark_repository import BookmarkRepository
from src.schemas.bookmark import BookmarkIn, BookmarkOut


router = APIRouter(tags=["bookmarks"])


@router.get("/bookmarks", response_model=list[BookmarkOut])
def my_bookmarks(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return BookmarkRepository(session).list_by_user(user.user_id)


@router.post("/books/{book_id}/bookmarks", response_model=BookmarkOut, status_code=201)
def create_bookmark(
    book_id: int,
    data: BookmarkIn,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if not BookRepository(session).get_by_id(book_id):
        raise HTTPException(404, "Книга не найдена")
    return BookmarkRepository(session).create(
        user_id=user.user_id,
        book_id=book_id,
        position=data.position,
        note=data.note,
    )


@router.delete("/bookmarks/{bookmark_id}", status_code=204)
def delete_bookmark(
    bookmark_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if not BookmarkRepository(session).delete(bookmark_id):
        raise HTTPException(404, "Закладка не найдена")