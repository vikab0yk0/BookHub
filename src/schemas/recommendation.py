from pydantic import BaseModel, ConfigDict
from src.schemas.book import BookShort


class RecommendationItemOut(BaseModel):
    book: BookShort
    score: float
    reason: str


class RecommendationListOut(BaseModel):
    user_id: int
    recommendations: list[RecommendationItemOut]