import os

ROOT_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE_PATH: str = os.path.join(ROOT_DIR, "config.yaml")
COOKIES_FILE_PATH: str = os.path.join(ROOT_DIR, "cookies.txt")
MESSAGES_DUMP_FILE_PATH: str = os.path.join(ROOT_DIR, "messages.dump")

__all__ = [
    "CONFIG_FILE_PATH",
    "COOKIES_FILE_PATH",
    "MESSAGES_DUMP_FILE_PATH",
    "ROOT_DIR",
]
