from .base import DTO
from src.db.models.channel_type import ChannelTypeEnum


class ChannelTypeBaseDTO(DTO):
    type: ChannelTypeEnum = ChannelTypeEnum.YOUTUBE


class ChannelTypeCreateDTO(ChannelTypeBaseDTO): ...


class ChannelTypeRetrieveDTO(ChannelTypeCreateDTO):
    id: int


__all__ = ["ChannelTypeRetrieveDTO"]
