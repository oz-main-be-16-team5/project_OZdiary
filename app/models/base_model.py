from tortoise import fields, Model


class BaseModel(Model):
    id = fields.BigIntField(primary_key=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True
