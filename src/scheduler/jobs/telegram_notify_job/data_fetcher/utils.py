def make_time_readable(seconds: float) -> str:
    """
    :param seconds:
    :return:
    """
    h = seconds // 3600
    m = (seconds - h * 3600) // 60
    s = seconds - (h * 3600) - (m * 60)
    return f"{h:0>2d}:{m:0>2d}:{s:0>2d}"


__all__ = ["make_time_readable"]
