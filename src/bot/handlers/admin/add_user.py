from aiogram import Bot
from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import BotCommandScopeChat
from aiogram.types import Chat
from aiogram.types import KeyboardButton
from aiogram.types import KeyboardButtonRequestUser
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import ReplyKeyboardRemove

from ...commands import user_commands
from ...filters import RoleFilter
from ...filters import UserRole
from src.db import DataAccessLayer
from src.db.models import UserModel
from src.db.models import UserRoleModel
from src.logger import logger

add_user_router = Router(name="acl")


@add_user_router.message(
    Command("add_user"),
    RoleFilter(role=[UserRole.ADMIN]),
)
async def add_user(message: Message, **kwargs):
    await message.answer(
        "Press button below to select user for adding.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="Select user",
                        request_user=KeyboardButtonRequestUser(
                            request_id=1234567890, user_is_bot=False
                        ),
                    ),
                ]
            ],
            is_persistent=False,
            one_time_keyboard=True,
        ),
    )


@add_user_router.message(
    F.user_shared,
    RoleFilter(role=[UserRole.ADMIN]),
)
async def handle_user(message: Message, bot: Bot, dal: DataAccessLayer, **kwargs):
    user_shared = message.user_shared
    if not user_shared:
        await message.answer(text="❌ No user shared.")
        return
    try:
        user_id = user_shared.user_id
        chat: Chat = await bot.get_chat(chat_id=user_id)

        user = UserModel(
            user_id=user_id,
            username=chat.username,
            firstname=chat.first_name,
            lastname=chat.last_name,
            role=UserRoleModel(role=UserRole.USER),
        )

        result = await dal.create_user(obj=user)
        if result:
            await bot.set_my_commands(
                user_commands(), scope=BotCommandScopeChat(chat_id=user.user_id)
            )
            await message.answer(
                text="Success. User added.", reply_markup=ReplyKeyboardRemove()
            )
        else:
            await message.answer(text="❌ Error during create. Try again.")

    except Exception as ex:
        await logger.aerror(str(ex))
        await message.reply(text="❌ UnknownError. Notify administrators.")
    finally:
        await message.answer(text="Finished", reply_markup=ReplyKeyboardRemove())


__all__ = ["add_user_router"]
