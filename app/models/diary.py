from app.models.base_model import BaseModel
from app.models.user import UserModel
from tortoise import fields


class DiaryModel(BaseModel):
    title = fields.CharField(max_length=255, null=False, description="일기 제목")
    content = fields.TextField(description="일기 내용")
    updated_at = fields.DatetimeField(auto_now=True)
    user: fields.ForeignKeyRelation[UserModel] = fields.ForeignKeyField(
        "models.UserModel",
        related_name="diaries",
        db_constraint=False,
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = "diaries"
