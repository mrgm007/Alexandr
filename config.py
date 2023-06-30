# group ids or account ids can be retrieved with @username_to_id_bot
from environs import Env

env = Env()
env.read_env()
BOT_TOKEN = "6188238802:AAGt8nI50W7uF2l_yefN9wUBeaArJtbLbUQ"
ADMIN = env.list("ADMINS")
IP = env.str("IP")


DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")