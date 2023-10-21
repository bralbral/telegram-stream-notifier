from urllib.parse import urlparse


def url_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False


__all__ = ["url_validator"]
