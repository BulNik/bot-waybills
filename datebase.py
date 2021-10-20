import sqlite3 as sl
import schedule
import time
import os

class DateBase():


    def __init__(self):
        self.db = sl.connect('users.db')
        self.cur = self.db.cursor()

    async def select_item_where_id(self, db, item, id):
        print(f"{__name__} {item} {id}")
        self.cur.execute(f"SELECT {item} FROM {db} WHERE id = {id}")
        #res = self.cur.fetchone()
        res = self.cur.fetchone()
        if res is not None:
            res = res[0]
        print(res)
        return res

    async def select_item_where_name(self, db, item, name):
        print(f"{__name__} {item} {id}")
        self.cur.execute(f"SELECT {item} FROM {db} WHERE name = '{name}'")
        res = self.cur.fetchone()[0]
        print(res)

        return res

    async def update_item_by_name(self, db, item, value, name):
        print(f"{__name__} {item} {value}")
        self.cur.execute(f"UPDATE {db} SET {item} = {value} WHERE name = '{name}'")
        self.db.commit()

    async def update_item_by_id(self, db, item, value, id):
        print(f"{__name__} {item} {value}")
        self.cur.execute(f"UPDATE {db} SET {item} = '{value}' WHERE id = '{id}'")
        self.db.commit()





    async def update_item_by_id_test(self, db, item, value, id):
        print(f"{id} {item} {value}")
        self.cur.execute(f"UPDATE {db} SET {item} = '{value}' WHERE id = '{id}'")
        self.db.commit()


