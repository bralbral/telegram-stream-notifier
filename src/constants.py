import os

ROOT_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE_PATH: str = os.environ.get(
    "CONFIG_FILE_PATH", os.path.join(ROOT_DIR, "config.yaml")
)

SQLITE_DATABASE_FILE_PATH: str = os.environ.get(
    "SQLITE_DATABASE_FILE_PATH", os.path.join(ROOT_DIR, "youtube-notifier-bot.db")
)
VERSION: str = "2024-09-24.07"

__all__ = [
    "CONFIG_FILE_PATH",
    "ROOT_DIR",
    "SQLITE_DATABASE_FILE_PATH",
    "VERSION",
]
