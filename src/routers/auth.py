from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.dependencies.db import get_session
from src.schemas.auth import RegisterIn, LoginIn, TokenOut
from src.schemas.user import UserOut
from src.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя",
)
def register(
    data: RegisterIn,
    session: Session = Depends(get_session),
):
    """Создаёт нового пользователя с ролью user."""
    auth = AuthService(session)
    try:
        user = auth.register(
            username=data.username,
            email=data.email,
            password=data.password,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    return user


@router.post(
    "/login",
    response_model=TokenOut,
    summary="Логин, получение JWT",
)
def login(
    data: LoginIn,
    session: Session = Depends(get_session),
):

    auth = AuthService(session)
    try:
        token = auth.login(
            email=data.email,
            password=data.password,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    return {"access_token": token, "token_type": "bearer"}