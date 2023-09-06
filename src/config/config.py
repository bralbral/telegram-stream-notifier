from pydantic import BaseModel
from pydantic import field_validator
from pydantic import SecretStr


class BotConfig(BaseModel):
    token: SecretStr
    chat_id: SecretStr

    @field_validator("chat_id", mode="before")
    def validate_chat_id(cls, v):
        return SecretStr(str(v))


class Channel(BaseModel):
    url: str
    label: str


class Config(BaseModel):
    bot: BotConfig
    channels: list[Channel]
    interval_s: int
    timezone: str
    fire_when_starts: bool = True


__all__ = ["BotConfig", "Config"]
