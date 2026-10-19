from typing import Optional
from sqlalchemy import select, inspect
from sqlalchemy.orm import Session
from src.models.user import User

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, username: str, email: str, password_hash: str, role_id: int) -> User:
        user = User(username=username, email=email, password_hash=password_hash, role_id=role_id)
        self.session.add(user)
        state = inspect(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_username(self, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username)
        return self.session.scalar(stmt)
