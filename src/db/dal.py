from .dao import ChannelDAO
from .dao import ChannelTypeDAO
from .dao import UserDAO
from .dao import UserRoleDAO
from .models import ChannelModel
from .models import UserModel
from .models.user_role import UserRole


class DataAccessLayer:
    def __init__(self) -> None:
        self.channel_dao = ChannelDAO()
        self.channel_type_dao = ChannelTypeDAO()
        self.user_dao = UserDAO()
        self.user_role_dao = UserRoleDAO()

    async def create_user(self, obj: UserModel) -> UserModel | None:
        user_role = obj.role
        user_role_instance, _ = await self.user_role_dao.get_or_create(
            role=user_role.role
        )
        obj.role = user_role_instance

        return await self.user_dao.create(obj=obj)

    async def get_user_by_pk(self, pk: int) -> UserModel | None:
        return await self.user_dao.get_first(id=pk)

    async def get_user_by_attr(self, *args, **kwargs) -> UserModel | None:
        return await self.user_dao.get_first(*args, **kwargs)

    async def list_users_by_attr(self, *args, **kwargs) -> list[UserModel]:
        return list(await self.user_dao.get_many(*args, **kwargs))

    async def is_admins_exists(self) -> bool:
        return bool(await self.list_users_by_attr(role=UserRole.ADMIN))

    async def get_users(self, admins: bool = False) -> list[int]:
        if admins:
            role = UserRole.ADMIN
        else:
            role = UserRole.USER

        role_instance, _ = await self.user_role_dao.get_or_create(role=role)
        users = await self.list_users_by_attr(role=role_instance)

        user_ids: list[int] = [user.user_id for user in users]
        return user_ids

    async def update_channel_by_id(self, obj: ChannelModel) -> int | None:
        channel = await self.channel_dao.update(obj=obj)
        if channel:
            return channel.id

        return None

    async def create_channel(self, obj: ChannelModel) -> ChannelModel | None:
        channel_type = obj.type
        channel_type_instance, _ = await self.channel_type_dao.get_or_create(
            type=channel_type.type
        )
        obj.type = channel_type_instance

        return await self.channel_dao.create(obj=obj)

    async def get_channels(self, *args, **kwargs) -> list[ChannelModel]:
        return list(await self.channel_dao.get_many(*args, **kwargs))

    async def delete_channel_by_id(self, id: int) -> int | None:
        result = await self.channel_dao.delete(id=id)
        return id if result else None


__all__ = ["DataAccessLayer"]
