from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# --- Diary Create ---
class CreateDiaryRequest(BaseModel):
    title: str = Field(..., max_length=255, description="일기 제목")
    content: Optional[str] = Field(None, description="일기 내용")


# --- Diary Read ---


class DiaryResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str | None
    created_at: datetime
    updated_at: datetime


# --- Diary Update ---


class UpdateDiaryRequest(BaseModel):
    title: str
    content: str | None


# --- Diary Delete ---


class DeleteDiaryResponse(BaseModel):
    id: int
