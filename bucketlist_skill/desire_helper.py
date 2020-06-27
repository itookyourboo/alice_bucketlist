import sqlite3
import os
from difflib import SequenceMatcher as sequence


def create_user_table():
    cursor.execute('create table if not exists user ('
                   'id integer primary key autoincrement, '
                   'user_id string not null);')


def create_desire_table():
    cursor.execute('create table if not exists desire ('
                   'id integer primary key autoincrement, '
                   'text string not null,'
                   'tags string,'
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
        cursor.execute(f"insert into user(user_id) values(?)", (user_id,))
        db.commit()

    @staticmethod
    def get_user(id_=None, user_id=None):
        if id_:
            return cursor.execute(f"select * from user where id = {id_}").fetchone()
        elif user_id:
            return cursor.execute(f"select * from user where user_id = '{user_id}'").fetchone()


class Desire:
    @staticmethod
    def add_to_user(usr_id, desire_id):
        id_, user_id = User.get_user(user_id=usr_id)
        cursor.execute("insert into user_desire(user_id, desire_id, completed) values(?, ?, ?)",
                       (id_, desire_id, 0))
        db.commit()

    @staticmethod
    def delete_desire(usr_id, desire_id):
        id_, user_id = User.get_user(user_id=usr_id)
        cursor.execute(f'delete from user_desire where user_id = {user_id} and desire_id = {desire_id}')
        db.commit()

    @staticmethod
    def add_desire(text, tags, usr_id):
        id_, user_id = User.get_user(user_id=usr_id)
        cursor.execute("insert into desire(owner_id, text, tags) values(?, ?, ?)",
                       (id_, text, tags))
        db.commit()

        desire_id, text, tags, owner_id = Desire.get_desire(text, usr_id)
        cursor.execute("insert into user_desire(user_id, desire_id, completed) values(?, ?, ?)",
                       (id_, desire_id, 0))
        db.commit()

    @staticmethod
    def complete_desire(usr_id, desire_id):
        id_, _ = User.get_user(user_id=usr_id)
        cursor.execute(f"update user_desire set completed = 1 where desire_id = {desire_id} and user_id = {id_}")
        db.commit()

    @staticmethod
    def get_desire(text, usr_id):
        id_, user_id = User.get_user(user_id=usr_id)
        return cursor.execute(f"select * from desire where text = '{text}' and owner_id = {id_}").fetchone()

    @staticmethod
    def get_desires(usr_id, local=False):
        id_, _ = User.get_user(user_id=usr_id)
        if local:
            return cursor.execute(f"select * from desire where id in ("
                                  f"select desire_id from user_desire where user_id = {id_})").fetchall()
        return cursor.execute(f"select * from desire where id not in "
                              f"(select desire_id from user_desire where user_id = {id_})").fetchall()

    @staticmethod
    def get_completed_desires(usr_id):
        id_, _ = User.get_user(user_id=usr_id)
        return cursor.execute(f"select * from desire where id in "
                              f"(select desire_id from user_desire where user_id = {id_} and completed = 1)").fetchall()

    @staticmethod
    def get_uncompleted_desires(usr_id):
        id_, _ = User.get_user(user_id=usr_id)
        return cursor.execute(f"select * from desire where id in "
                              f"(select desire_id from user_desire where user_id = {id_} and completed = 0)").fetchall()

    @staticmethod
    def how_many_added(desire_id):
        return cursor.execute(f"select count(*) from user_desire where desire_id = {desire_id}").fetchone()[0]

    @staticmethod
    def how_many_completed(desire_id):
        return cursor.execute(f"select count(*) from user_desire where "
                              f"desire_id = {desire_id} and completed = 1").fetchone()[0]

    @staticmethod
    def get_tags(count=5):
        lines = cursor.execute(f"select tags from desire").fetchall()
        tags = {}
        for line in lines:
            for t in line[0].split(','):
                if t in tags:
                    tags[t] += 1
                else:
                    tags[t] = 1
        return list(map(lambda x: x[0], sorted(tags.items(), key=lambda x: -x[1])))[:min(count, len(tags))]

    @staticmethod
    def find_by_tags(usr_id, tokens):
        res = []
        desires = Desire.get_desires(usr_id, local=False)
        for desire in desires:
            if any(x in desire[2] for x in tokens):
                res.append(desire)
                continue

        return res

    @staticmethod
    def get_random_desire(usr_id):
        id_, _ = User.get_user(user_id=usr_id)
        return cursor.execute(f"select * from desire where owner_id not in "
                              f"(select user_id from user_desire where user_id = {id_}) "
                              f"order by random() limit 1").fetchone()

    @staticmethod
    def find_by_text(usr_id, text):
        desires = Desire.get_desires(usr_id, local=True)
        mx = 0
        mx_desire = None
        for desire in desires:
            ratio = sequence(None, desire[1].lower(), text.lower()).ratio()
            if ratio > max(0.5, mx):
                mx = ratio
                mx_desire = desire

        return mx > 0.5, mx_desire
