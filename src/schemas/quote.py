from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class QuoteIn(BaseModel):
    quote_text: str = Field(min_length=1)
    page: int | None = Field(None, ge=1)


class QuoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    quote_id: int
    user_id: int
    book_id: int
    quote_text: str
    page: int | None
    created_at: datetime