import logging
import typing
from pyrogram.errors import InviteHashInvalid, UsernameInvalid, UsernameNotOccupied
from urllib.parse import urlparse

from src.bot.config import tracker_bot

logger = logging.Logger("Bot Agent Logger", level=logging.INFO)


async def join_chat(link_or_username: str) -> typing.Tuple[bool, typing.Optional[str]]:
    """
    Подписаться на канал или чат по ссылке или username.

    :param link_or_username: username (с @ или без), или ссылка на канал/группу
    :return: True если успешно подписались, False если ошибка
    """
    try:
        parsed = urlparse(link_or_username)

        if parsed.scheme in {"https", "http"} and "t.me" in parsed.netloc:
            chat_id = parsed.path.strip("/")
        elif 't.me' in parsed.path:
            chat_id = parsed.path.replace("t.me/", "")
        elif link_or_username.startswith("@"):
            chat_id = link_or_username[1:]
        else:
            chat_id = link_or_username

        await tracker_bot.join_chat(chat_id)
        logger.info(f"✅ Успешно подписался на: {chat_id}")
        return True, None

    except (UsernameInvalid, UsernameNotOccupied, InviteHashInvalid) as ex:
        logger.error(f"❌ Невалидная ссылка или username: {link_or_username} ({ex})")
        return False, str(ex)
    except Exception as ex:
        logger.error(f"❌ Ошибка при подписке: {ex}")
        return False, str(ex)
