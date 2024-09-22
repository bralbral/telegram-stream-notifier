import enum

from sqlmodel import Field

from .base import BaseSQLModel


class UserRole(enum.IntEnum):
    USER = 0
    ADMIN = 1


class UserModel(BaseSQLModel):

    __tablename__ = "users"

    user_id: int = Field(index=True)
    username: str = Field(max_length=255, nullable=True, index=True)
    firstname: str = Field(max_length=255, nullable=True, index=True)
    lastname: str = Field(max_length=255, nullable=True, index=True)
    user_role_id: int | None = Field(default=None, foreign_key="user_roles.id")


__all__ = ["UserModel"]
