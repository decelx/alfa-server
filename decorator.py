from russian_names import RussianNames
from time import time

import psycopg2
from config import load_config
from flask import Response


config = load_config('postgresql_db')

# app = Flask(__name__)

def connect():
    conn = psycopg2.connect(**config)
    return conn

def gen_time(func):
    def wrapped(*args, **kwargs):
        start_time = time()
        res = func(*args, **kwargs)
        total_time = time() - start_time

        print(f'Время выполнения фунцкии = {total_time}')
        return res
    return wrapped


def get_fio():
    name = RussianNames(count=1, patronymic=False, name=True, surname=False)
    batch1 = name.get_batch()
    surname = RussianNames(count=1, patronymic=False, name=False, surname=True)
    batch2 = surname.get_batch()
    patronymic = RussianNames(count=1, patronymic=True, name=False, surname=False)
    batch3 = patronymic.get_batch()
    for i in range(0, len(batch1)):
        print(batch1[i])
        print(batch2[i])
        print(batch3[i])


        try:
            conn = connect()
            cur = conn.cursor()
            cur.execute(f'''INSERT INTO public.gen_name (name, surname, patronymic) VALUES ('{batch1[i]}', '{batch2[i]}', '{batch3[i]}');''')
            conn.commit()
            conn.close()
            return Response('done', status=200)
        except Exception as error:
            print(error)
            return Response('fail', status=404)

@gen_time
def starter_fun():
    sch = 0
    while sch < 1:
        get_fio()
        sch += 1


starter_fun()


def del_use(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute(f"""DELETE FROM public.gen_name WHERE id='{id}'""")
    conn.commit()
    conn.close()

# del_use()


def creat_tabl():

    conn = connect()
    cur = conn.cursor()
    cur.execute(f'''CREATE TABLE IF NOT EXISTS test_gen_users (
                        id BIGINT NOT NULL PRIMARY KEY,
                        first_name NOT NULL,
                        last_name NOT NULL,
                        patronymic NOT NULL
                        );''')
    conn.commit()
    conn.close()

# creat_tabl()