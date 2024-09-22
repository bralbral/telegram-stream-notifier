import enum

from sqlalchemy import Column
from sqlalchemy import Enum
from sqlmodel import Field
from sqlmodel import Relationship

from . import UserModel
from .base import BaseSQLModel


class UserRole(enum.IntEnum):
    USER = 0
    SUPERUSER = 1
    UNKNOWN = -1


class UserRoleModel(BaseSQLModel):

    __tablename__ = "user_roles"

    role: UserRole = Field(
        sa_column=Column(
            Enum(UserRole), default=UserRole.USER, nullable=False, index=False
        )
    )

    users: list[UserModel] = Relationship(back_populates="role")


__all__ = ["UserRole", "UserRoleModel"]
