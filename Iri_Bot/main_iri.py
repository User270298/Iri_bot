from aiogram import Bot, Dispatcher
import asyncio
from settings import get_setting
import basic_iri
import logging
setting=get_setting('Input')
logger = logging.getLogger(__name__)


async def start():
    print('Bot run')
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')
    bot = Bot(token=setting.bots.bot_token, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_router(basic_iri.router)
    print('Bot run')
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())
