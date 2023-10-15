from pydantic import BaseModel
from pydantic import ConfigDict


class Schema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


__all__ = ["Schema"]
