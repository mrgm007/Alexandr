from aiogram import executor
from dispatcher import dp, db
import handlers

async def on_startup(dispatcher):
    #create connect to db
    await db.create()
    #create table from db
    await db.create_table_users()
    await db.create_table_button()
    await db.create_table_staff()
    await db.create_table_history()
    print("Connecting db and create tables: True")

if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True, on_startup=on_startup)