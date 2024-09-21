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


class YoutubeCredentials(BaseSettings):

    cookies_filepath: str


class TwitchCredentials(BaseSettings):
    """
    Credentials for TwitchApi
    https://dev.twitch.tv/docs/authentication/register-app/
    """

    app_id: str
    app_secret: str


class Config(BaseSettings):
    """
    All in one config
    """

    bot: BotConfig
    chat_id: int
    temp_chat_id: int
    report: Report
    start_scheduler: bool
    interval_s: int
    twitch: Optional[TwitchCredentials] = None
    youtube: Optional[YoutubeCredentials] = None


__all__ = ["BotConfig", "Config"]
