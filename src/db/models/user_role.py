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


class UserRole(enum.IntEnum):
    USER = 0
    SUPERUSER = 1
    UNKNOWN = -1


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
            Enum(UserRole), default=UserRole.USER, nullable=False, index=False
        )
    )

    users: list["UserModel"] = Relationship(
        back_populates="role",
    )


__all__ = ["UserRole", "UserRoleModel"]
