from typing import Union
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
import config

class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None
#Создаём подкючение и авторизацию к бд
    async def create(self):
        self.pool = await asyncpg.create_pool(user = config.DB_USER, password = config.DB_PASS, host = config.DB_HOST, database = config.DB_NAME)


#Тут мы принимаем и передаём команды
    async def execute(self, command, *args, fetch: bool = False, fetchval: bool = False, fetchrow: bool = False, execute: bool = False):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    # UNIQUE - вместо PRIMARY KEY
    async def  create_table_users(self):
        sql = """
        CREATE TABLE  IF NOT EXISTS users(
        user_id BIGINT NOT NULL PRIMARY KEY, 
        user_name  VARCHAR(255) NULL,
        full_name VARCHAR(255) NOT NULL, 
        status VARCHAR(255) NULL
        );
        """
        await self.execute(sql, execute=True)



    async def  create_table_button(self):
        sql = """
        CREATE TABLE  IF NOT EXISTS button_name(
        buttons  VARCHAR(255) NOT NULL PRIMARY KEY,
        category VARCHAR(255) NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def  create_table_staff(self):
        sql = """
        CREATE TABLE  IF NOT EXISTS staff(
        file_name  VARCHAR(255) NOT NULL,
        button_name VARCHAR(255) NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_history(self):
        sql = """
            CREATE TABLE  IF NOT EXISTS history(
            user_id BIGINT NOT NULL,
            user_name  VARCHAR(255) NULL,
            full_name VARCHAR(255) NOT NULL, 
            status VARCHAR(255) NULL,
            file_name  VARCHAR(255) NOT NULL,
            button_name VARCHAR(255) NOT NULL
            );
            """
        await self.execute(sql, execute=True)

# Вывести все данные из таблици users
    async def select_all_users(self):
        sql = "SELECT * FROM users"
        return await self.execute(sql, fetch=True)

# Вывести все данные из таблици history
    async def select_all_history(self):
        sql = "SELECT * FROM history"
        return await self.execute(sql, fetch=True)

# Удалить все данные из таблици history
    async def delete_all_history(self):
        sql = "DELETE FROM history WHERE TRUE"
        return await self.execute(sql, execute=True)


    @staticmethod
    def format_args(sql, parameters: dict):
        sql +=" AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)])
        return sql, tuple(parameters.values())

# Добавление юезра
    async def add_user(self, user_id, user_name, full_name):
        sql = "INSERT INTO users (user_id, user_name, full_name) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, user_id, user_name, full_name, fetchrow=True)


# Добавление истории
    async def add_history(self, user_id, user_name, full_name, status, file_name, button_name):
        sql = "INSERT INTO history (user_id, user_name, full_name, status, file_name, button_name) VALUES($1, $2, $3, $4, $5, $6) returning *"
        return await self.execute(sql, user_id, user_name, full_name, status, file_name, button_name, execute=True)

# Показать все данные из таблици history конкретного юзера
    async def show_history_user(self, user_id):
        sql = "SELECT * FROM history WHERE user_id=$1"
        return await self.execute(sql, user_id, fetch=True)

# Достаём юзера по какимто данным
    async def select_users(self, **kwargs):
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

# Вывести пользователей с определённым статусом
    async def select_user_for_status(self, status):
        sql = "SELECT * FROM users WHERE status=$1"
        return await self.execute(sql, status, fetch=True)

# Получения статуса пользователя
    async def get_status_user(self, user_id):
        sql = "SELECT status FROM users WHERE user_id=$1"
        return await self.execute(sql, user_id, fetchrow=True)

# Удаляем определённого user
    async def delete_user(self, user_id):
        sql = "DELETE FROM users WHERE user_id=$1"
        return await self.execute(sql, user_id, fetchrow=True)


# Добавляем статус
    async def add_status_for_user(self, status, user_id):
        sql = "UPDATE users SET status=$1 WHERE user_id=$2"
        return await self.execute(sql, status, user_id, execute=True)

# Добавление стафа  в бд
    async def add_staff_in_db(self, file_name, button_name):
        sql = "INSERT INTO staff (file_name, button_name) VALUES($1, $2) returning *"
        for line in file_name.split('\n'):
            await self.execute(sql, line, button_name, execute=True)

# Достаём стаф из бд по кнопке
    async def get_staff_in_db(self, button_name):
        sql = "SELECT file_name FROM staff WHERE button_name=$1"
        return await self.execute(sql, button_name, fetchrow=True)

    async def get_count_staff_in_db(self, button_name):
        sql = "SELECT COUNT(file_name) FROM staff WHERE button_name = $1"
        return await self.execute(sql, button_name, fetchrow=True)


# Удаляем стаф который уже взяли
    async def delete_user_staff(self, file_name):
        sql = "DELETE FROM staff WHERE file_name=$1"
        return await self.execute(sql, file_name, fetchrow=True)

#Добавление кнопки
    async def add_button_file_id(self, buttons, category):
        sql = "INSERT INTO button_name (buttons, category) VALUES($1, $2)"
        await self.execute(sql, buttons, category, execute=True)

# Выводим все кнопки в определённой категории
    async def select_buttons(self, category):
        sql = "SELECT buttons FROM button_name WHERE category=$1"
        return await self.execute(sql, category, fetch=True)

    # Удаляем определённую кнопку
    async def delete_buttons(self, buttons):
        sql = "DELETE FROM button_name WHERE buttons=$1"
        await self.execute(sql, buttons, execute=True)


def logger(statement):
        print(f"""
    ----------------------------------------------------------------------- 
    Executing:
    {statement}
    -----------------------------------------------------------------------
        """)

