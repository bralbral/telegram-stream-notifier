from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Report(BaseSettings):
    template: str | None
    empty: str | None


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


class DatabaseConfig(BaseSettings):
    """
    PostgreSQL database configuration
    """

    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: SecretStr
    database: str = "youtube_notifier"

    @property
    def url(self) -> str:
        return (
            f"postgres://{self.user}:{self.password.get_secret_value()}@"
            f"{self.host}:{self.port}/{self.database}"
        )


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
    admin_id: int
    database: DatabaseConfig | None = None
    twitch: TwitchCredentials | None = None
    youtube: YoutubeCredentials | None = None


__all__ = ["BotConfig", "Config", "DatabaseConfig"]
