from src.utils import youtube_channel_url_validator

GOOD_URL = "https://www.youtube.com/@gtrfmusic"
MALFORMED_URL = "https://www.youtube.com/@gtrfmusic?si=23213173713"


def test_url_validation():
    assert youtube_channel_url_validator(GOOD_URL) is True
    assert youtube_channel_url_validator(MALFORMED_URL) is False
