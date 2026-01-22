from app.models.base_model import BaseModel
from app.models.user import UserModel
from app.models.question import QuestionModel
from tortoise import fields


class UserQuestionModel(BaseModel):
    user: fields.ForeignKeyRelation[UserModel] = fields.ForeignKeyField(
        "models.UserModel",
        related_name="user_questions",
        db_constraint=False,
        on_delete=fields.CASCADE,
    )
    questions: fields.ForeignKeyRelation[QuestionModel] = fields.ForeignKeyField(
        "models.QuestionModel",
        related_name="user_questions",
        db_constraint=False,
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = "user_questions"
