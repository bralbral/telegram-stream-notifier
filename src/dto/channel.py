from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator

from .base import DTO


class ChannelBaseDTO(DTO):
    url: str = Field(max_length=255)
    label: str = Field(max_length=255)
    user_id: int
    enabled: bool

    model_config = ConfigDict(from_attributes=True)

    @field_validator("url")
    def url_in_username(cls, v: str) -> str:
        if "/@" not in v:
            raise ValueError(
                "Url must be contain @username: https://www.youtube.com/@username"
            )

        return v.lower()


class ChannelCreateDTO(ChannelBaseDTO):
    ...


class ChannelRetrieveDTO(ChannelCreateDTO):
    id: int

    def to_html(self) -> str:
        return (
            f"<b>id</b>:{self.id}<br/>"
            f"<b>label</b>:{self.label}<br/>"
            f"<b>url</b>:{self.url}<br/>"
            f"<b>enabled</b>:{self.enabled}<br/>"
        )


__all__ = ["ChannelCreateDTO", "ChannelRetrieveDTO"]
