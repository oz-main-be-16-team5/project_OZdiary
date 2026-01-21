from tortoise import fields
from app.models.base_model import BaseModel


class QuestionModel(BaseModel):
    """
    questions 테이블에 대응되는 tortoise ORM 모델
    """

    question_text = fields.TextField(description="스크래핑 질문")

    class Meta:
        table = "questions"
