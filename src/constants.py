import os

ROOT_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE_PATH: str = os.environ.get(
    "CONFIG_FILE_PATH", os.path.join(ROOT_DIR, "config.yaml")
)

POSTGRES_CONNECTION_URL: str = os.environ.get(
    "POSTGRES_CONNECTION_URL", "sqlite://db.sqlite3"
)
VERSION: str = "2026-05-22.19"

__all__ = [
    "CONFIG_FILE_PATH",
    "POSTGRES_CONNECTION_URL",
    "ROOT_DIR",
    "VERSION",
]
