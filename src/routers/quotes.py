from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.dependencies.auth import get_current_user
from src.dependencies.db import get_session
from src.models.user import User
from src.repositories.book_repository import BookRepository
from src.repositories.quote_repository import QuoteRepository
from src.schemas.quote import QuoteIn, QuoteOut


router = APIRouter(tags=["quotes"])


@router.get("/quotes", response_model=list[QuoteOut])
def my_quotes(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return QuoteRepository(session).list_by_user(user.user_id)


@router.post("/books/{book_id}/quotes", response_model=QuoteOut, status_code=201)
def create_quote(
    book_id: int,
    data: QuoteIn,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if not BookRepository(session).get_by_id(book_id):
        raise HTTPException(404, "Книга не найдена")
    return QuoteRepository(session).create(
        user_id=user.user_id,
        book_id=book_id,
        quote_text=data.quote_text,
        page=data.page,
    )


@router.delete("/quotes/{quote_id}", status_code=204)
def delete_quote(
    quote_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if not QuoteRepository(session).delete(quote_id):
        raise HTTPException(404, "Цитата не найдена")