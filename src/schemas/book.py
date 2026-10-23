from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class BookCreate(BaseModel):

    title: str = Field(min_length=1, max_length=255)
    author: str = Field(min_length=1, max_length=255)
    genre: str | None = Field(None, max_length=100)
    annotation: str | None = None
    content: str | None = None


class BookUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    author: str | None = Field(None, min_length=1, max_length=255)
    genre: str | None = Field(None, max_length=100)
    annotation: str | None = None
    content: str | None = None


class BookShort(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    book_id: int
    title: str
    author: str
    genre: str | None


class BookFull(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    book_id: int
    title: str
    author: str
    genre: str | None
    annotation: str | None
    content: str | None
    created_by: int | None
    created_at: datetime
    updated_at: datetime