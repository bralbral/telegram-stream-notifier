from __future__ import annotations

from tortoise import fields
from tortoise.models import Model


class ChannelModel(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    url = fields.CharField(max_length=255, unique=True, index=True)
    label = fields.CharField(max_length=255, index=True)
    enabled = fields.BooleanField(index=True)
    user: fields.ForeignKeyRelation["UserModel"] = fields.ForeignKeyField(  # noqa: F821
        "models.UserModel", related_name="channels", null=True, on_delete=fields.CASCADE
    )
    type: fields.ForeignKeyRelation["ChannelTypeModel"] = fields.ForeignKeyField(  # noqa: F821
        "models.ChannelTypeModel", related_name="channels", on_delete=fields.CASCADE
    )

    def to_html(self) -> str:
        user_attribute_list = [self.user.username, self.user.user_id]
        attribute = next(item for item in user_attribute_list if item is not None)
        user_link = f'<a href="{self.user.get_url_generated_by_id}">{attribute}</a>'

        return (
            f"📺 <b>Selected channel</b>: <br/>"
            f"├──<b>type</b>: <b>{self.type.type}</b><br/>"
            f"├──<b>enabled</b>: <b>{self.enabled}</b><br/>"
            f"├──<b>id</b>: {self.id}<br/>"
            f"├──<b>label</b>: {self.label}<br/>"
            f"├──<b>url</b>: {self.url}<br/>"
            f"├──<b>added by</b>: {user_link}<br/>"
            f"├──<b>added at</b>: {self.created_at}<br/>"
            f"└──<b>last modified at</b>: {self.updated_at}<br/>"
        )

    class Meta:
        table = "channels"


__all__ = ["ChannelModel"]
