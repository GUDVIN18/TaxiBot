from config import DB_NAME
from peewee import SqliteDatabase

db = SqliteDatabase(DB_NAME)
db.execute_sql('create table if not exists user (id INTEGER PRIMARY KEY, user_id INTEGER);')
db.execute_sql('create table if not exists settings (id INTEGER PRIMARY KEY, bot_password TEXT);')
db.execute_sql('create table if not exists filter (id INTEGER PRIMARY KEY, user_id INTEGER, price INTEGER, '
               'classes TEXT, date TEXT, time INTEGER);')
db.execute_sql('create table if not exists orders (id INTEGER PRIMARY KEY, order_id INTEGER);')
