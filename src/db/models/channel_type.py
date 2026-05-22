from __future__ import annotations

from typing import TYPE_CHECKING

import enum

from tortoise import fields
from tortoise.models import Model

if TYPE_CHECKING:
    from .channel import ChannelModel


class ChannelType(str, enum.Enum):
    YOUTUBE = "YOUTUBE"
    TWITCH = "TWITCH"
    KICK = "KICK"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class ChannelTypeModel(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    type = fields.CharEnumField(
        ChannelType, default=ChannelType.YOUTUBE, max_length=15, unique=True
    )

    channels: fields.ReverseRelation[ChannelModel]

    class Meta:
        table = "channel_types"


__all__ = ["ChannelType", "ChannelTypeModel"]
