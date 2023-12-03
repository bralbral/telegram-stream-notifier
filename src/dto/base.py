from pydantic import BaseModel
from pydantic import ConfigDict


class DTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)


__all__ = ["DTO"]
