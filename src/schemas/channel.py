from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator


class ChannelSchema(BaseModel):
    id: int
    url: str = Field(max_length=255)
    label: str = Field(max_length=255)
    enabled: bool

    class Config:
        orm_mode = True

    @field_validator("url")
    def name_must_contain_space(cls, v: str) -> str:
        if "/@" not in v:
            raise ValueError(
                "Url must be contain @username: https://www.youtube.com/@username"
            )

        return v.lower()


__all__ = ["ChannelSchema"]
