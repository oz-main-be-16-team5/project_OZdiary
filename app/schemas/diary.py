from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# --- Diary Create ---
class CreateDiaryRequest(BaseModel):
    title: str = Field(..., max_length=255,
                       description="일기 제목",
                       examples=["오늘의 일기"]
    )
    content: Optional[str] = Field(
        None,
        description="일기 내용",
        examples=["아침에 운동하고 FastAPI"]
    )


# --- Diary Read ---


class DiaryResponse(BaseModel):
    id: int = Field(..., examples=[1])
    user_id: int = Field(..., examples=[10])
    title: str = Field(..., examples=["오늘의 일기"])
    content: str | None = Field(
        None,
        examples=["내용입니다"]
    )
    created_at: datetime = Field(
        ...,
        examples=["2026-01-22T09:00:00"]
    )
    updated_at: datetime = Field(
        ...,
        examples=["2026-01-22T09:30:00"]
    )

# --- Diary Update ---


class UpdateDiaryRequest(BaseModel):
    title: str = Field(..., examples=["수정된 제목"])
    content: str | None = Field(
        None,
        examples=["수정된 내용"]
    )

# --- Diary Delete ---


class DeleteDiaryResponse(BaseModel):
    id: int
