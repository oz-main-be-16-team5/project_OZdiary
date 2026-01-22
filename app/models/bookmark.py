from app.models.base_model import BaseModel
from app.models.user import UserModel
from app.models.quote import QuoteModel
from tortoise import fields


class BookmarkModel(BaseModel):
    user: fields.ForeignKeyRelation[UserModel] = fields.ForeignKeyField(
        "models.UserModel",
        related_name="bookmarks",
        db_constraint=True,
        on_delete=fields.CASCADE,
    )
    quote: fields.ForeignKeyRelation[QuoteModel] = fields.ForeignKeyField(
        "models.QuoteModel",
        related_name="bookmarks",
        db_constraint=True,
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = "bookmarks"
        unique_together = ("user", "quote")
