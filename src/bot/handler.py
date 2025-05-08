import logging

from pyrogram import filters

from src.bot.config import tracker_bot

logger = logging.getLogger(__name__)


@tracker_bot.on_message()
async def echo_message(client, message):
    print(message)