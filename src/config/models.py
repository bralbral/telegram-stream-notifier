from typing import Optional

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Report(BaseSettings):
    template: Optional[str]
    empty: Optional[str]


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
    superuser_id: int
    temp_chat_id: int
    report: Report
    channels: list[Channel]
    interval_s: int


__all__ = ["BotConfig", "Channel", "Config"]
