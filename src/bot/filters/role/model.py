from enum import Enum


class UserRole(Enum):
    SUPERUSER = "superuser"
    ADMIN = "admin"
    UNKNOWN = "unknown"

    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.value


__all__ = ["UserRole"]
