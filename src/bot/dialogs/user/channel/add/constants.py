from src.db.models.channel_type import ChannelType
from src.utils import kick_channel_url_validator
from src.utils import twitch_channel_url_validator
from src.utils import youtube_channel_url_validator

url_validators: dict = {
    ChannelType.YOUTUBE: youtube_channel_url_validator,
    ChannelType.TWITCH: twitch_channel_url_validator,
    ChannelType.KICK: kick_channel_url_validator,
}

url_examples: dict = {
    ChannelType.YOUTUBE: "https://www.youtube.com/@username",
    ChannelType.TWITCH: "https://www.twitch.tv/username",
    ChannelType.KICK: "empty",
}

__all__ = ["url_examples", "url_validators"]
