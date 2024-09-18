from datetime import datetime

from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator

from .base import DTO
from .channel_type import ChannelTypeBaseDTO
from .user import UserRetrieveDTO


class ChannelBaseDTO(DTO):
    url: str = Field(max_length=255)
    label: str = Field(max_length=255)
    user_id: int
    enabled: bool
    type: ChannelTypeBaseDTO

    model_config = ConfigDict(from_attributes=True)

    @field_validator("url")
    def url_in_username(cls, v: str) -> str:
        if "/@" not in v:
            raise ValueError(
                "Url must be contain @username: https://www.youtube.com/@username"
            )

        return v.lower()


class ChannelCreateDTO(ChannelBaseDTO): ...


class ChannelRetrieveDTO(ChannelCreateDTO):
    id: int
    user: UserRetrieveDTO
    created_at: datetime
    updated_at: datetime

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


__all__ = ["ChannelCreateDTO", "ChannelRetrieveDTO"]
