from typing import Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    user_id: int
    username: Optional[str]
    firstname: Optional[str]
    lastname: Optional[str]
    is_admin: bool
    is_superuser: bool

    class Config:
        orm_mode = True


__all__ = ["UserSchema"]
