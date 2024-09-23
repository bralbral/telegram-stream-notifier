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
    from .channel import ChannelModel


class ChannelType(enum.IntEnum):
    YOUTUBE = 0
    TWITCH = 1


class ChannelTypeModel(SQLModel, table=True):

    __tablename__ = "channel_types"
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
    type: ChannelType = Field(
        sa_column=Column(
            Enum(ChannelType),
            default=ChannelType.YOUTUBE,
            nullable=False,
            index=False,
            unique=True,
        )
    )

    channels: list["ChannelModel"] = Relationship(back_populates="type")


__all__ = ["ChannelTypeModel"]
