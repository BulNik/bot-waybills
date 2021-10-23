import asyncio
import datetime
import logging
from aiogram import Bot, Dispatcher
from aiogram.utils.exceptions import ChatNotFound, BotBlocked
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from common import register_handlers_common
from state import register_handlers_choose
from datebase import DateBase

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger.error("Starting bot")
bot = Bot(token="2086919077:AAFUj0PJ55qLtcccXOfwPKtxKHKhO_WQwUE")
dp = Dispatcher(bot, storage=MemoryStorage())



async def main():
    register_handlers_choose(dp)
    register_handlers_common(dp)

    #await set_commands(bot)
    await dp.start_polling()

async def run_check(bot):
    sql = DateBase()
    f_time = datetime.timedelta(days=2)
    s_time = datetime.timedelta(days=1)
    e_time = datetime.timedelta(days=0)
    f_msg = "Ваша подписка истекает через 2 дня"
    s_msg = "Ваша подписка истекает через 1 день"
    e_msg = "Ваша подписка истекла, обратитесь к администратору для продления подписки"
    while True:
        sql.cur.execute("SELECT id, until FROM users")
        for id, until in sql.cur.fetchall():
            now = datetime.datetime.now().strftime('%d-%m-%Y')
            now = datetime.datetime.strptime(now, '%d-%m-%Y')
            until = datetime.datetime.strptime(until, '%d-%m-%Y')
            delta = until - now
            try:
                if delta < e_time:
                    await bot.send_message(id, e_msg)
                    #await asyncio.sleep(86400)
                elif delta < s_time:
                    await bot.send_message(id, s_msg)
                    #await asyncio.sleep(86400)
                elif delta < f_time:
                    await bot.send_message(id, f_msg)
                    #await asyncio.sleep(86400)
            except ChatNotFound:
                print(f"Пользователь с id {id} не начинал диалог с ботом")
                #await asyncio.sleep(86400)
            except BotBlocked:
                print(f"Пользователь с id {id} заблокировал бота")
                await asyncio.sleep(86400)
        await asyncio.sleep(86400)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    try:
        asyncio.ensure_future(main())
        asyncio.ensure_future(run_check(bot=Bot(token="2086919077:AAFUj0PJ55qLtcccXOfwPKtxKHKhO_WQwUE")))
        loop.run_forever()
    finally:
        print("Close")
        loop.close()







