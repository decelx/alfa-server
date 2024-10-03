from flask import request

# import psycopg2
# from config import load_config
#
# config = load_config('postgresql_db')
#
#
# def connect():
#     conn = psycopg2.connect(**config)
#     return conn
#
#
# try:
#     conn = connect()
#     cur = conn.cursor()
    # cur.execute(f'''CREATE TABLE IF NOT EXISTS public."pg_test3"
    #     (
    #         name text COLLATE pg_catalog."default",
    #         surname text COLLATE pg_catalog."default",
    #         patronymic text COLLATE pg_catalog."default"
    #     )
    #
    #     TABLESPACE pg_default;
    #
    #     ALTER TABLE IF EXISTS public."pg_test3"
    #         OWNER to postgres;''')
#     cur.execute('''SELECT name, surname, patronymic FROM public.pg_test;''')
#     # conn.commit()
#     conn.close()
# except Exception as error:
#     print(error)

