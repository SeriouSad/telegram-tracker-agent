from pyrogram import Client

from src.settings import settings

tracker_bot = Client(
    settings.bot_session_name,
    api_id=settings.api_id,
    api_hash=settings.api_hash,
)
