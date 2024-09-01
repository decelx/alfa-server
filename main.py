# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask import request
import psycopg2
from config import load_config
from flask import Response
from urllib.parse import urlparse

# conStr = "localhost://postgres:password@data_quality:5432"
# p = urlparse(conStr)
#
# pg_connection_dict = {
#     'dbname': p.hostname,
#     'user': p.username,
#     'password': p.password,
#     'port': p.port,
#     'host': p.scheme
# }

# print(pg_connection_dict)
# con = psycopg2.connect(**pg_connection_dict)
# print(con)
config = load_config('postgresql_db')

app = Flask(__name__)

def connect():
    conn = psycopg2.connect(**config)
    return conn





@app.route('/')
def hello():
    config = load_config('postgresql_db')
    return render_template('index.html')


@app.route('/check-user-data', methods=['POST'])
def checkUser():
    if request.method == 'POST':
        user = request.json['email']
        password = request.json['password']

        print('hello')

        conn = connect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users;')
        users = cur.fetchall()
        conn.close()

        if user == users[0][2] and password == users[0][1]:
            return Response('done', status=200)
        else:
            return Response('fail', status=404)


@app.route('/test')
def test():
    return render_template('butn.html')


@app.route('/testtt')
def test2():
    return render_template('test.html')




if __name__ == '__main__':
    app.run(debug=True)