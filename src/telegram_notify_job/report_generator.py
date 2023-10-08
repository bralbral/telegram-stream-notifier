from typing import Optional

from jinja2 import Template

from .schemas import ChannelDescription


def generate_jinja_report(
    data: list[ChannelDescription], report_template: str, empty_template: Optional[str]
) -> Optional[str]:
    """
    :param empty_template:
    :param report_template:
    :param data:
    :return:
    """

    if len(data) > 0:
        template = Template(report_template)
    else:
        if not empty_template:
            return None

        template = Template(empty_template)

    result = template.render(channels=data)

    return result


__all__ = ["generate_jinja_report"]
