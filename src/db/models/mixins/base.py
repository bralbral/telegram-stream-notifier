from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class ModelORM(AsyncAttrs, DeclarativeBase):
    pass


__all_ = ["ModelORM"]
