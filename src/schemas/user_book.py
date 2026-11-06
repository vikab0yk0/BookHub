from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict


class UserBookIn(BaseModel):
    status: Literal["favorite", "read", "planned"]


class UserBookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    book_id: int
    status: str
    added_at: datetime