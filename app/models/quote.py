from tortoise import fields
from app.models.base_model import BaseModel


class QuoteModel(BaseModel):
    """
    명언(Quote) 모델
    """

    content = fields.TextField(description="명언 내용")
    author = fields.CharField(
        max_length=100,
        null=True,
        description="작성자",
    )

    class Meta:
        table = "quotes"
