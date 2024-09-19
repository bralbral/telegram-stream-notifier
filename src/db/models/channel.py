from sqlmodel import Field

from .base import BaseModel


class ChannelModel(BaseModel, table=True):

    __tablename__ = "channels"

    url: str = Field(max_length=255, nullable=False, index=True)
    label: str = Field(max_length=255, nullable=False, index=True)
    enabled: bool = Field(nullable=False, index=True)
    user_id: int | None = Field(default=None, foreign_key="users.id")
    channel_type_id: int | None = Field(default=None, foreign_key="channel_types.id")


__all__ = ["ChannelModel"]
