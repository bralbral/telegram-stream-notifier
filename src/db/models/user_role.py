import enum
from datetime import datetime
from typing import Optional
from typing import TYPE_CHECKING

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel


if TYPE_CHECKING:
    from .user import UserModel


class UserRole(enum.StrEnum):
    USER = "USER"
    SUPERUSER = "SUPERUSER"
    UNKNOWN = "UNKNOWN"


class UserRoleModel(SQLModel, table=True):

    __tablename__ = "user_roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            default=datetime.utcnow,
            nullable=False,
        )
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
        )
    )
    role: "UserRole" = Field(
        sa_column=Column(
            Enum(UserRole, length=15),
            default=UserRole.USER,
            nullable=False,
            index=False,
            unique=True,
        )
    )

    users: list["UserModel"] = Relationship(back_populates="role", cascade_delete=True)


__all__ = ["UserRole", "UserRoleModel"]
