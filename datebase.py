import sqlite3 as sl
import schedule
import time
import os

class DateBase():


    def __init__(self):
        self.db = sl.connect('users.db')
        print(f"Статус подключения БД {os.path.exists('users.db')}")
        self.cur = self.db.cursor()
        self.cur.execute(f"SELECT * FROM users")
        print(self.cur.fetchone())

        # Создание бд с проверкой на наличие
        '''
        with self.db:
            self.db.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id INTEGER,
                            name TEXT,
                            phone_number TEXT,
                            password TEXT,
                            probeg TEXT,
                            status TEXT,
                            dogovor TEXT,
                            start_at TEXT,
                            end_at TEXT,
                            sub INTEGER,
                            until TEXT 
                        );
                    """)
        '''
            #self.db.commit()



    def check_sub_job(self):
        """
        sql = DateBase()
        f_time = datetime.timedelta(days=2)
        s_time = datetime.timedelta(days=1)
        e_time = datetime.timedelta(days=1)
        f_msg = "Ваша подписка истекает через 2 дня"
        s_msg = "Ваша подписка истекает через 1 день"
        e_msg = "Ваша подписка истекал, обратитесь к админестратору для продления подписки "
        """
        print("Проверка")
        """
        sql.cur.execute("SELECT id, until FROM users")
        for id, until in sql.cur.fetchall():
            now = datetime.datetime.now().strftime('%d-%m-%Y')
            now = datetime.datetime.strptime(now, '%d-%m-%Y')
            until = datetime.datetime.strptime(until, '%d-%m-%Y')
            delta = until - now
            if delta < e_time:
                await bot.send_message(id, e_msg)
            elif delta < s_time:
                await bot.send_message(id, s_msg)
            elif delta < f_time:
                await bot.send_message(id, f_msg)
        """

    async def run_check(self):
        schedule.every(5).seconds.do(self.check_sub_job)
        while True:
            self.stat = 1
            schedule.run_pending()
            self.stat = None
            time.sleep(1)
