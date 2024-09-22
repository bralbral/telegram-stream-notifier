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

from ...commands import user_commands
from ...filters import RoleFilter
from ...filters import UserRole
from ...states import UsersSG
from src.db import DataAccessLayer
from src.db.models import UserModel
from src.logger import logger

add_user_router = Router(name="acl")


@add_user_router.message(
    Command("add_user"),
    RoleFilter(role=[UserRole.SUPERUSER]),
    State(state="*"),
)
async def add_user(message: Message, state: FSMContext, **kwargs):
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


@add_user_router.message(
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

        user = UserModel(
            user_id=user_id,
            username=chat.username,
            firstname=chat.first_name,
            lastname=chat.last_name,
            is_superuser=False,
        )

        result = await dal.create_user(obj=user)
        if result:
            await bot.set_my_commands(
                user_commands(), scope=BotCommandScopeChat(chat_id=user.user_id)
            )

            await message.answer(text="Success. User added.")
        else:
            await message.answer(text="Error during create. Try again.")

    except (Exception,) as ex:
        await logger.aerror(str(ex))
        await message.reply(text=f"❌ UnknownError. Notify administrators. Thank you!")
    finally:
        await state.clear()
        await message.answer(text="Finished", reply_markup=ReplyKeyboardRemove())


__all__ = ["add_user_router"]
