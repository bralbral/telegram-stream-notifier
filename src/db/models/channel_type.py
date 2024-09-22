import enum
from typing import TYPE_CHECKING

from sqlalchemy import Column
from sqlalchemy import Enum
from sqlmodel import Field
from sqlmodel import Relationship

from .base import BaseSQLModel

if TYPE_CHECKING:
    from .channel import ChannelModel


class ChannelType(enum.IntEnum):
    YOUTUBE = 0
    TWITCH = 1


class ChannelTypeModel(BaseSQLModel):

    __tablename__ = "channel_types"

    type: ChannelType = Field(
        sa_column=Column(
            Enum(ChannelType), default=ChannelType.YOUTUBE, nullable=False, index=False
        )
    )

    channels: list["ChannelModel"] = Relationship(back_populates="type")


__all__ = ["ChannelTypeModel"]
