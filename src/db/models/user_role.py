from __future__ import annotations

import enum

from tortoise import fields
from tortoise.models import Model


class UserRole(str, enum.Enum):
    USER = "USER"
    SUPERUSER = "SUPERUSER"
    UNKNOWN = "UNKNOWN"


class UserRoleModel(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    role = fields.CharEnumField(UserRole, default=UserRole.USER, max_length=15, unique=True)

    users: fields.ReverseRelation["UserModel"]  # noqa: F821

    class Meta:
        table = "user_roles"


__all__ = ["UserRole", "UserRoleModel"]
