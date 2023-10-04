from typing import Optional

from jinja2 import Template

from .schemas import ChannelDescription


def generate_report(data: list[ChannelDescription]) -> Optional[str]:
    """
    :param data:
    :return:
    """
    msg_header = f"""
       <h1>✅ СЕЙЧАС В ЭФИРЕ:</h1>
       <br/>
       """
    msg_footer = f"""
       <hr/>
       <i>Powered by <a href='https://t.me/diskordovoselo'>DiskordovoSelo</a></i>
       """

    msg_body = ""

    if data:
        msg_body += "<ol type='1'>"
        for cd in data:
            entry_body = ""

            entry_body += f"<b><a href='{cd.url}'>{cd.label}</a></b> <br/>"
            if cd.concurrent_view_count:
                entry_body += f"<b>👀 Cмотрят: {cd.concurrent_view_count}</b> <br/>"

            if cd.like_count:
                entry_body += f"<b>👍 Понравилось: {cd.like_count}</b> <br/>"

            if cd.duration:
                entry_body += f"<b>🕑 Длительность: {cd.duration}</b> <br/>"

            entry_body = "<li>" + entry_body + "</li>"
            entry_body += "<br/>"

            msg_body += entry_body

        msg_body += "</ol>"

    if msg_body:
        message_text = msg_header + msg_body + msg_footer
    else:
        message_text = None

    return message_text


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


__all__ = ["generate_jinja_report", "generate_report"]
