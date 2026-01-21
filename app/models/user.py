from tortoise import fields
from tortoise.models import Model


class UserModel(Model):
    user_id = fields.IntField(pk=True)
    username = fields.CharField(
        max_length=50, unique=True, description="User's username"
    )
    password_hash = fields.CharField(max_length=255, description="User's password")
    email = fields.CharField(
        max_length=255, unique=True, description="User's email address"
    )
    is_active = fields.BooleanField(default=True, description="User's active status")
    updated_at = fields.DatetimeField(
        auto_now=True
    )  # auto_now = 수정될 때마다 자동으로 지금 시간으로 바꿔라

    class Meta:
        table = "users"
