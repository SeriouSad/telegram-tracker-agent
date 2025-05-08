import uvicorn

from src.api.v1.app import app
from src.bot.handler import tracker_bot
from src.settings import settings
import asyncio


async def start_api():
    config = uvicorn.Config(app=app, host=settings.host, port=settings.port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


async def start_bot():
    await tracker_bot.start()


async def main():
    bot_task = asyncio.create_task(start_bot())
    api_task = asyncio.create_task(start_api())

    await asyncio.gather(bot_task, api_task)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()


