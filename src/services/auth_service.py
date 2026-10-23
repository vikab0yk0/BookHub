from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.config import settings
from src.models.user import User
from src.repositories.user_repository import UserRepository


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, session: Session):
        self.session = session
        self.user_repo = UserRepository(session)


    @staticmethod
    def hash_password(password: str) -> str:

        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, password_hash: str) -> bool:
        return pwd_context.verify(plain_password, password_hash)


    @staticmethod
    def create_token(user: User) -> str:
        payload = {
            "sub": str(user.user_id),        # subject — ID пользователя
            "role": user.role.name,           # роль: admin / user
            "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes),
            "iat": datetime.now(timezone.utc),
        }
        return jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )

    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        try:
            return jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            return None

    def register(self, username: str, email: str, password: str) -> User:
        if self.user_repo.get_by_username(username):
            raise ValueError(f"Пользователь '{username}' уже существует")
        if self.user_repo.get_by_email(email):
            raise ValueError(f"Email '{email}' уже занят")

        password_hash = self.hash_password(password)
        return self.user_repo.create(
            username=username,
            email=email,
            password_hash=password_hash,
            role_id=2,
        )

    def login(self, email: str, password: str) -> str:
        user = self.user_repo.get_by_email(email)
        if not user:
            raise ValueError("Неверный email или пароль")
        if not self.verify_password(password, user.password_hash):
            raise ValueError("Неверный email или пароль")

        return self.create_token(user)