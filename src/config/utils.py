import yaml

from .config import Config


def load_config(filepath: str) -> Config:
    """
    :param filepath:
    :return:
    """

    with open(file=filepath, encoding="utf-8") as fh:
        conf = Config(**yaml.safe_load(fh))

    return conf


__all__ = [
    "load_config",
]
