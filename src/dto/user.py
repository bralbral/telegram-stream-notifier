from typing import Optional

from pydantic import ConfigDict

from .base import DTO


class UserBaseDTO(DTO):
    user_id: int
    username: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    is_superuser: bool

    @property
    def get_url_generated_by_id(self) -> str:
        return f"tg://openmessage?user_id={self.user_id}"

    model_config = ConfigDict(from_attributes=True)


class UserCreateDTO(UserBaseDTO):
    ...


class UserRetrieveDTO(UserCreateDTO):
    id: int


__all__ = ["UserCreateDTO", "UserRetrieveDTO"]
