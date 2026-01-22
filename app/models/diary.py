from __future__ import annotations

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
        db_constraint=True,
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = "diaries"

    # CREATE
    @classmethod
    async def create_diary(cls, user_id: int, title: str, content: str) -> DiaryModel:
        return await cls.create(user_id=user_id, title=title, content=content)

    # READ
    @classmethod
    async def get_by_id(cls, diary_id: int) -> DiaryModel | None:
        return await cls.filter(id=diary_id).get_or_none()

    @classmethod
    async def get_all_by_user(cls, user_id: int) -> list[DiaryModel]:
        return await cls.filter(user_id=user_id).order_by("-created_at").all()

    # UPDATE
    @classmethod
    async def update_diary_title(cls, diary_id: int, title: str) -> int:
        return await cls.filter(id=diary_id).update(title=title)

    @classmethod
    async def update_diary_content(cls, diary_id: int, content: str) -> int:
        return await cls.filter(id=diary_id).update(content=content)

    # DELETE
    @classmethod
    async def delete_diary(cls, diary_id: int) -> int:
        return await cls.filter(id=diary_id).delete()
