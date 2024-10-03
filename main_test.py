# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask import request
import psycopg2
from config import load_config
from flask import Response
from gen_name import *

config = load_config('postgresql_db')

app = Flask(__name__)

def connect():
    conn = psycopg2.connect(**config)
    return conn


@app.route("/")
def index():
    return "привет"




@app.route('/index', methods=['POST'])
def checkUser():
    if request.method == 'POST':


        try:
            conn = connect()
            cur = conn.cursor()
            cur.execute("CREATE TABLE table_test(name, surname, patronymic)")
            conn.commit()
            conn.close()
            return Response('done', status=200)
        except Exception as error:
            print(error)
            return Response('fail', status=404)


@app.route('/test')
def test2():
    return render_template('html_test.html')


if __name__ == '__main__':
    app.run(debug=True)