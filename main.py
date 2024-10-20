# -*- coding: utf-8 -*-


from flask import Flask, render_template
from flask import request
import psycopg2
from config import load_config
from flask import Response
from urllib.parse import urlparse
from uuid import *
from gen_name import *
from credit_calc import Calculator


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
        surname_x = request.json['surname']
        name_x = request.json['name']
        father = request.json['father']
        # docsType = request.json['docsType']
        # for i in range(500):
        #
        #     id = uuid4()

        print("!!!")
        try:
            conn = connect()
            cur = conn.cursor()
            cur.execute(f'''INSERT INTO public.reference(surname, name, father) VALUES ('{surname_x}', '{name_x}','{father}');''')
            conn.commit()
            conn.close()
            return Response('done', status=200)
        except Exception as error:
            print(error)
            return Response('fail', status=500)


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

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')


@app.route('/credit_calc', methods = ["POST"])
def credit_calc():
    if request.method == 'POST':
        age = request.json['age']
        married = request.json['married']
        job = request.json['job']

        calc = Calculator(age, married, job)
        return calc.calculate()

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
                    <td><button class="btn btn-danger btn-lg">отправить</button></td>
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

@app.route('/window')
def window():
    return render_template('window.html')



if __name__ == '__main__':
    app.run(debug=True)
