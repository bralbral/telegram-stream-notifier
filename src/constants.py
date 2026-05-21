import os

ROOT_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE_PATH: str = os.environ.get(
    "CONFIG_FILE_PATH", os.path.join(ROOT_DIR, "config.yaml")
)
VERSION: str = "2026-05-19.14"

__all__ = [
    "CONFIG_FILE_PATH",
    "ROOT_DIR",
    "VERSION",
]
