# -*- coding: utf-8 -*-


from flask import Flask, render_template
from flask import request
import psycopg2
from config import load_config
from flask import Response
from urllib.parse import urlparse
from uuid import *

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
    return render_template('patternA.html')


@app.route('/index', methods=['POST'])
def checkUser():
    if request.method == 'POST':
        surname = request.json['surname']
        name = request.json['name']
        father = request.json['father']
        docsType = request.json['docsType']

        id = uuid4()

        
        try:
            conn = connect()
            cur = conn.cursor()
            cur.execute(f"INSERT INTO public.reference(surname, name, father, id, docstype) VALUES ('{surname}', '{name}', '{father}', '{id}', '{docsType}');")
            conn.commit()
            conn.close()
            return Response('done', status=200)
        except Exception as error:
            print(error)
            return Response('fail', status=404)


        #
        # try:
        #     if user == users[0][2] and password == users[0][1]:
        #         return Response('done', status=200)
        #     else:
        #
        # except Exception as error:
        #     print(error)


# @app.route('/main')
# def test():
#     return render_template('patternA.html')


@app.route('/application')
def test2():
    return render_template('application.html')



@app.route('/autorize', methods=['POST'])
def checkUserAlfa():
    if request.method == 'POST':
        name = request.json['name']
        password = request.json['password']
        # id = request.json['id']
        print(name, password)


        try:
            conn = connect()
            cur = conn.cursor()
            cur.execute(f'''INSERT INTO public."usersAlfa" (name, password) VALUES ('{name}', '{password}');''')
            conn.commit()
            conn.close()
            return Response('done', status=200)
        except Exception as error:
            print(error)
            return Response('fail', status=404)

@app.route('/user')
def test3():
    return render_template('user.html')

@app.route('/gen_table', methods = ["POST"])
def gen_table():
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM public.reference")
        referenses = cur.fetchall()
        conn.close()

        print(referenses)

        count = 1
        table_html = ""
        for ref in referenses:
            tr = f"""
                <tr>
                    <th scope="row">{count}</th>
                    <td>{ref[0]}</td>
                    <td>{ref[1]}</td>
                    <td>{ref[2]}</td>
                    <td>{ref[3]}</td>
                    <td>Кнопка</td>
                </tr>
            """
            table_html += tr
            count += 1
        return Response(table_html, status=200)
    except Exception as error:
        print(error)
        return Response('fail', status=404)

@app.route('/table')
def table():
    return render_template('table.html')



if __name__ == '__main__':
    app.run(debug=True)
