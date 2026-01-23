from pydantic import BaseModel
from datetime import datetime


# --- Quote Create ---
class CreateQuoteRequest(BaseModel):
    content: str
    author: str | None = None


# --- Quote Read ---
class QuoteResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    content: str
    author: str | None
    created_at: datetime


# --- Quote Delete ---
class DeleteQuoteResponse(BaseModel):
    id: int


# --- Bookmark (Response만 있으면 충분) ---
class BookmarkResponse(BaseModel):
    message: str
    quote_id: int
