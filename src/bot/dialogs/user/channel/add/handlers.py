from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from sulguk import SULGUK_PARSE_MODE

from src.bot.states import ChannelCreateSG
from src.db import DataAccessLayer
from src.db.models import ChannelModel
from src.db.models.channel_type import ChannelType


async def url_handler(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
    **kwargs,
) -> None:

    url = message.text.lower().strip()
    url_validator = dialog_manager.dialog_data["url_validator"]
    dal: DataAccessLayer = dialog_manager.dialog_data["dal"]

    if url_validator(url):
        dialog_manager.dialog_data["url"] = url

        obj = await dal.channel_dao.get_first(**{"url": url})
        if obj:
            await message.answer(
                f"❌ Channel <b>{url}</b> already exists with label <b>{obj.label}</b>. <br/>"
                f"Please set different <b>url</b> or <b>/cancel</b> for reject.",
                parse_mode=SULGUK_PARSE_MODE,
            )
            return

        await dialog_manager.switch_to(ChannelCreateSG.url_selected)


async def label_handler(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
    **kwargs,
) -> None:
    label = message.text.strip()
    url = dialog_manager.dialog_data["url"]
    if url and label:
        dal: DataAccessLayer = dialog_manager.dialog_data["dal"]

        user_obj = await dal.get_user_by_attr(**{"user_id": message.from_user.id})
        if user_obj:

            selected_channel_type = dialog_manager.dialog_data["selected_channel_type"]
            channel_type = ChannelType(selected_channel_type)
            channel_type_obj, _ = await dal.channel_type_dao.get_or_create(
                type=channel_type
            )

            channel = ChannelModel(
                url=url,
                label=label,
                enabled=True,
                user=user_obj,
                type=channel_type_obj,
            )

            result = await dal.create_channel(obj=channel)
            if result:
                await message.answer(
                    f"✅ Created. <br/> "
                    f"<code>#id: {result.id}<br/>"
                    f"label: {result.label}<br/>"
                    f"url:{result.url} </code>",
                    parse_mode=SULGUK_PARSE_MODE,
                )
            else:
                await message.answer(
                    f" ❌ Cannot add channel with parameters:<br/>"
                    f"<code>label: {label}<br/>"
                    f"url:{url} </code><br/>"
                    f"Contact admins.",
                    parse_mode=SULGUK_PARSE_MODE,
                )

        await dialog_manager.done()


__all__ = ["label_handler", "url_handler"]
