from datetime import datetime
from typing import Optional
from typing import TYPE_CHECKING

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel


if TYPE_CHECKING:
    from .channel_type import ChannelTypeModel
    from .user import UserModel


class ChannelModel(SQLModel):

    __tablename__ = "channels"

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
    url: str = Field(max_length=255, nullable=False, index=True)
    label: str = Field(max_length=255, nullable=False, index=True)
    enabled: bool = Field(nullable=False, index=True)
    user_id: int | None = Field(default=None, foreign_key="users.id")
    channel_type_id: int | None = Field(default=None, foreign_key="channel_types.id")

    user: "UserModel" = Relationship(back_populates="channels")
    type: "ChannelTypeModel" = Relationship(back_populates="channels")

    def to_html(self) -> str:

        user_attribute_list = [self.user.username, self.user.user_id]
        attribute = next(item for item in user_attribute_list if item is not None)
        user_link = f'<a href="{self.user.get_url_generated_by_id}">{attribute}</a>'

        return (
            f"📺 <b>Selected channel</b>: <br/>"
            f"├──<b>enabled</b>: <b>{self.enabled}</b><br/>"
            f"├──<b>id</b>: {self.id}<br/>"
            f"├──<b>label</b>: {self.label}<br/>"
            f"├──<b>url</b>: {self.url}<br/>"
            f"├──<b>added by</b>: {user_link}<br/>"
            f"├──<b>added at</b>: {self.created_at}<br/>"
            f"└──<b>last modified at</b>: {self.updated_at}<br/>"
        )


__all__ = ["ChannelModel"]
