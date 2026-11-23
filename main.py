import asyncio
from config.bot_config import bot, dp
from core.startup import on_startup
from database.db import create_table
import logging
from handlers import basic, stats
from handlers import vps
from worker import worker

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(name)s | %(levelname)s |%(message)s")

async def main():
    logger.info("Starting bot..")
    dp.startup.register(on_startup)
    dp.include_routers(basic.router, stats.router, vps.router)
    create_table()
    asyncio.create_task(worker(bot))
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot started")
    await dp.start_polling(bot) #type: ignore

if __name__ == "__main__":
    asyncio.run(main())
