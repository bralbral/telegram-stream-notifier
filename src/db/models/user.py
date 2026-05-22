from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.models import Model

if TYPE_CHECKING:
    from .channel import ChannelModel
    from .user_role import UserRoleModel


class UserModel(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    user_id = fields.IntField(unique=True, index=True)
    username = fields.CharField(max_length=255, null=True, index=True)
    firstname = fields.CharField(max_length=255, null=True, index=True)
    lastname = fields.CharField(max_length=255, null=True, index=True)
    role: fields.ForeignKeyRelation[UserRoleModel] = fields.ForeignKeyField(
        "models.UserRoleModel", related_name="users", on_delete=fields.CASCADE
    )

    created_channels: fields.ReverseRelation[ChannelModel]
    subscribed_channels: fields.ManyToManyRelation[ChannelModel]

    @property
    def get_url_generated_by_id(self) -> str:
        return f"tg://openmessage?user_id={self.user_id}"

    class Meta:
        table = "users"


__all__ = ["UserModel"]
