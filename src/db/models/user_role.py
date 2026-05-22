from __future__ import annotations

from typing import TYPE_CHECKING

import enum

from tortoise import fields
from tortoise.models import Model

if TYPE_CHECKING:
    from .user import UserModel


class UserRole(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"

    @classmethod
    def list(cls):
        return [cls.USER, cls.ADMIN]


class UserRoleModel(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    role = fields.CharEnumField(
        UserRole, default=UserRole.USER, max_length=15, unique=True
    )

    users: fields.ReverseRelation[UserModel]

    class Meta:
        table = "user_roles"


__all__ = ["UserRole", "UserRoleModel"]
