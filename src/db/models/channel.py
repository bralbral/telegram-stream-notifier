from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.models import Model

if TYPE_CHECKING:
    from .channel_type import ChannelTypeModel
    from .user import UserModel


class ChannelModel(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    url = fields.CharField(max_length=255, unique=True, index=True)
    label = fields.CharField(max_length=255, index=True)
    enabled = fields.BooleanField(index=True)
    creator: fields.ForeignKeyRelation[UserModel] | None = fields.ForeignKeyField(
        "models.UserModel",
        related_name="created_channels",
        null=True,
        on_delete=fields.SET_NULL,
    )
    type: fields.ForeignKeyRelation[ChannelTypeModel] = fields.ForeignKeyField(
        "models.ChannelTypeModel", related_name="channels", on_delete=fields.CASCADE
    )
    subscribers: fields.ManyToManyRelation[UserModel] = fields.ManyToManyField(
        "models.UserModel",
        related_name="subscribed_channels",
        through="channel_subscribers",
    )

    def to_html(self) -> str:
        creator_text = "unknown"
        if self.creator:
            user_attribute_list = [self.creator.username, self.creator.user_id]
            attribute = next(
                (item for item in user_attribute_list if item is not None), "unknown"
            )
            creator_text = (
                f'<a href="{self.creator.get_url_generated_by_id}">{attribute}</a>'
            )

        return (
            f"📺 <b>Selected channel</b>: <br/>"
            f"├──<b>type</b>: <b>{self.type.type}</b><br/>"
            f"├──<b>enabled</b>: <b>{self.enabled}</b><br/>"
            f"├──<b>id</b>: {self.id}<br/>"
            f"├──<b>label</b>: {self.label}<br/>"
            f"├──<b>url</b>: {self.url}<br/>"
            f"├──<b>created by</b>: {creator_text}<br/>"
            f"├──<b>created at</b>: {self.created_at}<br/>"
            f"└──<b>last modified at</b>: {self.updated_at}<br/>"
        )

    class Meta:
        table = "channels"


__all__ = ["ChannelModel"]
