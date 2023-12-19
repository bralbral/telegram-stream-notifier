from enum import Enum


class UserRole(Enum):
    SUPERUSER = "superuser"
    USER = "user"
    UNKNOWN = "unknown"

    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.value


__all__ = ["UserRole"]
