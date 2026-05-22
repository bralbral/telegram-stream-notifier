import os
from .dal import DataAccessLayer
from .exceptions import DatabaseDoesNotExist

# Build database URL from environment variables
_db_host = os.environ.get("DATABASE_HOST", "localhost")
_db_port = os.environ.get("DATABASE_PORT", "5432")
_db_user = os.environ.get("DATABASE_USER", "postgres")
_db_password = os.environ.get("DATABASE_PASSWORD", "postgres")
_db_name = os.environ.get("DATABASE_NAME", "youtube_notifier")

TORTOISE_ORM = {
    "connections": {
        "default": (
            f"postgres://{_db_user}:{_db_password}@" f"{_db_host}:{_db_port}/{_db_name}"
        )
    },
    "apps": {
        "models": {
            "models": ["src.db.models"],
            "default_connection": "default",
        },
    },
}

__all__ = ["DataAccessLayer", "DatabaseDoesNotExist", "TORTOISE_ORM"]
