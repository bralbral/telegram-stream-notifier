import os

ROOT_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE_PATH: str = os.environ.get(
    "CONFIG_FILE_PATH", os.path.join(ROOT_DIR, "config.yaml")
)
COOKIES_FILE_PATH: str = os.environ.get(
    "COOKIES_FILE_PATH", os.path.join(ROOT_DIR, "cookies.txt")
)
SQLITE_DATABASE_FILE_PATH: str = os.environ.get(
    "SQLITE_DATABASE_FILE_PATH", os.path.join(ROOT_DIR, "youtube-notifier-bot.db")
)
VERSION: str = "2024-06-20.10"

__all__ = [
    "CONFIG_FILE_PATH",
    "COOKIES_FILE_PATH",
    "ROOT_DIR",
    "SQLITE_DATABASE_FILE_PATH",
    "VERSION",
]
