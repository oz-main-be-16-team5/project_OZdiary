from pydantic import BaseModel
from datetime import datetime


# --- Question Create ---

class CreateQuestionRequest(BaseModel):
    question_text: str


# --- Question Read ---

class QuestionResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    question_text: str
    created_at: datetime

# --- Question Delete ---

class DeleteQuestionResponse(BaseModel):
    id: int
