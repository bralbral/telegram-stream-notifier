from pydantic import SecretStr
from pydantic_settings import BaseSettings


class BotConfig(BaseSettings):
    """
    Bot config
    """

    token: SecretStr


class Channel(BaseSettings):
    url: str
    label: str


class Config(BaseSettings):
    """
    All in one config
    """

    bot: BotConfig
    chat_id: int
    channels: list[Channel]
    interval_s: int


__all__ = ["BotConfig", "Channel", "Config"]
