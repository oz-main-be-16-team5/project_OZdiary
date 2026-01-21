from pydantic import BaseModel
from datetime import datetime


# --- Diary Create ---
class CreateDiaryRequest(BaseModel):
    user_id: int
    title: str
    content: str | None


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
