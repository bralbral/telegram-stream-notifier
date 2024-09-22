from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlmodel import Relationship

from .base import BaseSQLModel

if TYPE_CHECKING:
    from .channel import ChannelModel
    from .user_role import UserRoleModel


class UserModel(BaseSQLModel):

    __tablename__ = "users"

    user_id: int = Field(index=True)
    username: str = Field(max_length=255, nullable=True, index=True)
    firstname: str = Field(max_length=255, nullable=True, index=True)
    lastname: str = Field(max_length=255, nullable=True, index=True)
    user_role_id: int | None = Field(default=None, foreign_key="user_roles.id")

    role: "UserRoleModel" = Relationship(back_populates="users")
    channels: list["ChannelModel"] = Relationship(back_populates="user")

    @property
    def get_url_generated_by_id(self) -> str:
        return f"tg://openmessage?user_id={self.user_id}"


__all__ = ["UserModel"]
