from typing import Optional

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


__all__ = ["generate_report"]
