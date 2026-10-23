from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class BookmarkIn(BaseModel):
    position: int = Field(ge=0)
    note: str | None = None


class BookmarkOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    bookmark_id: int
    user_id: int
    book_id: int
    position: int
    note: str | None
    created_at: datetime