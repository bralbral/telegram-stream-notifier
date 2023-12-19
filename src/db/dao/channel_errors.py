from sqlalchemy import func
from sqlalchemy import insert
from sqlalchemy import select

from ..models import ChannelErrorORM
from ..models import ChannelORM
from .base import DAO
from src.dto import ChannelErrorCreateDTO


class ChannelErrorDAO(DAO):
    async def create(self, channel_error_schema: ChannelErrorCreateDTO) -> int:
        insert_stmt = (
            insert(ChannelErrorORM)
            .values(**channel_error_schema.model_dump())
            .returning(ChannelErrorORM.id)
        )
        await self.session.execute(insert_stmt)
        result = await self.session.execute(insert_stmt)
        _id: int = result.scalars().one()
        return _id

    async def get_channel_ids_with_errors_upper_then_limit(
        self, limit: int
    ) -> list[int]:
        channel_sub = select(ChannelORM.id).where(ChannelORM.enabled == True).distinct()

        stm = (
            select(ChannelErrorORM.channel_id, func.count(ChannelErrorORM.channel_id))
            .where(ChannelErrorORM.channel_id.in_(channel_sub))
            .group_by(ChannelErrorORM.channel_id)
        ).having(func.count(ChannelErrorORM.channel_id) > limit)

        res = await self.session.scalars(statement=stm)
        ids = res.all()
        return list(ids)


__all__ = ["ChannelErrorDAO"]
