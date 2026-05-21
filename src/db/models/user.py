from __future__ import annotations

from tortoise import fields
from tortoise.models import Model


class UserModel(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    user_id = fields.IntField(unique=True, index=True)
    username = fields.CharField(max_length=255, null=True, index=True)
    firstname = fields.CharField(max_length=255, null=True, index=True)
    lastname = fields.CharField(max_length=255, null=True, index=True)
    role: fields.ForeignKeyRelation["UserRoleModel"] = fields.ForeignKeyField(  # noqa: F821
        "models.UserRoleModel", related_name="users", on_delete=fields.CASCADE
    )

    channels: fields.ReverseRelation["ChannelModel"]  # noqa: F821

    @property
    def get_url_generated_by_id(self) -> str:
        return f"tg://openmessage?user_id={self.user_id}"

    class Meta:
        table = "users"


__all__ = ["UserModel"]
