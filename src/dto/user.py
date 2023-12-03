from typing import Optional

from pydantic import ConfigDict

from .base import DTO


class UserBaseDTO(DTO):
    user_id: int
    username: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    is_admin: bool
    is_superuser: bool

    model_config = ConfigDict(from_attributes=True)


class UserCreateDTO(UserBaseDTO):
    ...


class UserRetrieveDTO(UserCreateDTO):
    id: int


__all__ = ["UserCreateDTO", "UserRetrieveDTO"]
