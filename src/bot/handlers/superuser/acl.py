from aiogram import Bot
from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import BotCommandScopeChat
from aiogram.types import Chat
from aiogram.types import KeyboardButton
from aiogram.types import KeyboardButtonRequestUser
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import ReplyKeyboardRemove

from ...commands import admin_commands
from ...filters import RoleFilter
from ...filters import UserRole
from ...states import UsersSG
from src.db import DataAccessLayer
from src.dto import UserDTO

acl_router = Router(name="acl")


@acl_router.message(
    Command("promote"),
    RoleFilter(role=[UserRole.SUPERUSER]),
    State(state="*"),
)
async def promote_user_to_admin(message: Message, state: FSMContext, **kwargs):
    await message.answer(
        "See keyboard below. Select User for add.",
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
    await state.set_state(UsersSG.promote)


@acl_router.message(
    F.user_shared,
    RoleFilter(role=[UserRole.SUPERUSER]),
    StateFilter(UsersSG.promote),
)
async def handle_user(
    message: Message, state: FSMContext, bot: Bot, dal: DataAccessLayer, **kwargs
):
    try:
        user_id = message.user_shared.user_id
        chat: Chat = await bot.get_chat(chat_id=user_id)

        user_dto = UserDTO(
            user_id=user_id,
            username=chat.username,
            firstname=chat.first_name,
            lastname=chat.last_name,
            is_admin=True,
            is_superuser=False,
        )

        result = await dal.create_user(user_schema=user_dto)
        if result:
            await bot.set_my_commands(
                admin_commands(), scope=BotCommandScopeChat(chat_id=user_dto.user_id)
            )

            await message.answer(text="Success")
        else:
            await message.answer(text="Error")
    except Exception as ex:
        print(ex)
    finally:
        await state.clear()
        await message.answer(text="Finished", reply_markup=ReplyKeyboardRemove())


@acl_router.message(
    Command("revoke"),
    RoleFilter(role=[UserRole.SUPERUSER]),
    State(state="*"),
)
async def revoke_user(message: Message, **kwargs):
    await message.answer("Deleted.")


__all__ = ["acl_router"]
