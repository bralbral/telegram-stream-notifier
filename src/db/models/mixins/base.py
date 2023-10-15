from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class ModelOrm(AsyncAttrs, DeclarativeBase):
    pass


__all_ = ["ModelOrm"]
