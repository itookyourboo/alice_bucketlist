import sqlite3
import os


def create_user_table():
    cursor.execute('create table if not exists user ('
                   'id integer primary key autoincrement, '
                   'user_id string not null);')


def create_desire_table():
    cursor.execute('create table if not exists desire ('
                   'id integer primary key autoincrement, '
                   'text string not null,'
                   'tags string,'
                   'published integer not null,'
                   'owner_id integer);')


def create_user_desire_table():
    cursor.execute('create table if not exists user_desire ('
                   'id integer primary key autoincrement,'
                   'user_id integer not null,'
                   'desire_id integer not null,'
                   'completed integer not null);')


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')

db = sqlite3.connect(DB_PATH)
cursor = db.cursor()

create_user_table()
create_desire_table()
create_user_desire_table()
db.commit()


class User:
    @staticmethod
    def user_exists(user_id):
        return cursor.execute(f"select * from user where user_id = '{user_id}'").fetchone() is not None

    @staticmethod
    def add_user(user_id):
        if User.user_exists(user_id):
            return
        cursor.execute(f"insert into user(user_id) values(?)", user_id)
        db.commit()

    @staticmethod
    def get_user(id_=None, user_id=None):
        if id_:
            return cursor.execute(f"select * from user where id = {id_}").fetchone()
        elif user_id:
            return cursor.execute(f"select * from user where user_id = '{user_id}'").fetchone()


class Desire:
    @staticmethod
    def offer_desire(text, usr_id):
        id_, user_id = User.get_user(user_id=usr_id)
        cursor.execute("insert into desire (text, owner_id, published) values(?, ?, ?)",
                       (text, id_, 0))
        db.commit()

    @staticmethod
    def add_published_desire(text, tags, usr_id):
        id_, user_id = User.get_user(user_id=usr_id)
        cursor.execute("insert into desire (text, tags, owner_id, published) values(?, ?, ?)",
                       (text, tags, id_, 1))
        db.commit()

    @staticmethod
    def my_desires(usr_id, tags=''):
        id_, user_id = User.get_user(user_id=usr_id)
        cursor.execute("insert")

    @staticmethod
    def get_tags(count=5, published=True):
        pub = '2' if published else '0 or published = 1'
        tags = []
        desires = cursor.execute(f"select tags from desire where published = {pub}")
