from datetime import datetime

from pydantic import ConfigDict
from pydantic import Field

from .base import DTO
from .channel import ChannelRetrieveDTO


class ChannelErrorBaseDTO(DTO):
    error: str = Field(max_length=512)

    model_config = ConfigDict(from_attributes=True)


class ChannelErrorCreateDTO(ChannelErrorBaseDTO):
    channel_id: int


class ChannelErrorRetrieveDTO(ChannelErrorCreateDTO):
    id: int
    channel: ChannelRetrieveDTO
    created_at: datetime
    updated_at: datetime


__all__ = ["ChannelErrorCreateDTO", "ChannelErrorRetrieveDTO"]
