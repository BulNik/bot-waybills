import asyncio
import datetime
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.utils.exceptions import ChatNotFound, BotBlocked
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from common import register_handlers_common
from state import register_handlers_choose
from datebase import DateBase

logger = logging.getLogger(__name__)

async def main():
    #print(os.getcwd())
    #print(os.listdir(os.getcwd()))
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    # Объявление и инициализация объектов бота и диспетчера
    #bot = Bot(token="1876416438:AAHDb9Fe4Ow5AlhVH-FB-gHfdeVCqdeefTg")
    bot = Bot(token="2086919077:AAFUj0PJ55qLtcccXOfwPKtxKHKhO_WQwUE")
    dp = Dispatcher(bot, storage=MemoryStorage())

    sql = DateBase()

    # Регистрация хэндлеров
    register_handlers_choose(dp)
    register_handlers_common(dp)

    # Установка команд бота
    #await set_commands(bot)

    # Запуск поллинга
    await dp.start_polling()
    #await run_check()



async def check_if_notifications_are_needed():
    print("Проверка")
    pass

#а ниже будет что-то типа
async def run_check(bot):
    sql = DateBase()
    f_time = datetime.timedelta(days=2)
    s_time = datetime.timedelta(days=1)
    e_time = datetime.timedelta(days=0)
    f_msg = "Ваша подписка истекает через 2 дня"
    s_msg = "Ваша подписка истекает через 1 день"
    e_msg = "Ваша подписка истекал, обратитесь к админестратору для продления подписки "
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
                elif delta < s_time:
                    await bot.send_message(id, s_msg)
                elif delta < f_time:
                    await bot.send_message(id, f_msg)
            except ChatNotFound:
                print(f"Пользователь с id {id} не начинал диалог с ботом")
            except BotBlocked:
                print(f"Пользователь с id {id} заблокировал бота")


        await asyncio.sleep(10)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(main())
        asyncio.ensure_future(run_check(bot=Bot(token="2086919077:AAFUj0PJ55qLtcccXOfwPKtxKHKhO_WQwUE")))
        loop.run_forever()
    finally:
        print("Close")
        loop.close()






