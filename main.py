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
from model import User
from flask_sqlalchemy import SQLAlchemy


config = load_config('postgresql_db')

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:decel99@127.0.0.1:5432/postgres"

db = SQLAlchemy()
db.init_app(app)

with app.app_context():
    db.create_all()

def connect():
    conn = psycopg2.connect(**config)
    return conn


def get_20(num=1):
    conn = connect()
    cur = conn.cursor()
    cur.execute(f'''SELECT * FROM public.reference''')
    referenses = cur.fetchall()
    conn.close()

    count = 0
    answer = []
    for i in referenses:
        count += 1

        # if count >= ((num - 1) * 20) and count <= (num * 20):
        answer.append(i)
    return answer



@app.route('/')
def hello():
    # new_user = User(2, '123', 'acd')
    # db.session.add(new_user)
    # db.session.commit()
    return render_template('patternA.html')


@app.route('/index', methods=['POST'])
def checkUser():
    if request.method == 'POST':
        surname_x = request.json['surname']
        name_x = request.json['name']
        father = request.json['father']
        reference = request.json['reference']
        docsType = request.json['docsType']
        id = uuid4()
        # docsType = request.json['docsType']
        # for i in range(500):
        #


        print("!!!")
        try:
            conn = connect()
            cur = conn.cursor()
            cur.execute(f'''INSERT INTO public.reference(surname, name, father, reference, id, document) VALUES ('{surname_x}', '{name_x}','{father}', '{reference}', '{id}', '{docsType}');''')
            print(reference)
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
    user = db.session.get(User, 1)
    user1 = User(3, '543', '123@mail.ru')
    db.session.add(user1)
    db.session.commit()
    return render_template('calculator.html')


@app.route('/credit_calc', methods=["POST"])
def credit_calc():
    print(request.json)
    if request.method == 'POST':
        age = int(request.json['age'])
        if request.json['married'] == 'Женат':
            married = True
        else:
            married = False
        if request.json['job'] == 'Работаю':
            job = True
        else:
            job = False

        calc = Calculator(age, married, job)
        print(calc.calculate())
        return Response(str(calc.calculate()), status=200)

@app.route('/gen_table/', methods = ["POST"])
def gen_table():
    if request.method == 'POST':
        num = request.json['num']

        try:
            referenses = get_20(num)
            count = 1
            table_html = ""
            for ref in referenses:
                tr = f"""
                    <tr>
                        <th scope="row">{count}</th>
                        <td class="surname">{ref[0]}</td>
                        <td class="name">{ref[1]}</td>
                        <td class="father">{ref[2]}</td>
                        <td class="ref">{ref[3]}</td>
                        <td class="doc">{ref[5]}</td>
                        <td><button type="button" class="btn btn-danger btn-lg print-btn" data-toggle="modal" data-target="#staticBackdrop" style="background: #e80000;">Печать</button></td>
                    </tr>    
                """
                table_html += tr
                count += 1
            return Response(table_html, status=200)
        except Exception as error:
            print(error)
            return Response('fail', status=404)

@app.route('/del_user', methods = ["POST"])
def del_user():
    conn = connect()
    cur = conn.cursor()
    cur.execute(f'''SELECT id FROM public.reference''')
    id = cur.fetchall()
    table_html = ""
    for i in id:
        tr = f"""
            <tr>
                <td class="id">{i}</td>
                <td><button type="button" class="btn btn-danger btn-lg print-btn" data-toggle="modal" data-target="#staticBackdrop" style="background: #e80000;">Удолить</button></td>
            </tr>
        """
        table_html += tr
        print(table_html)
    conn.close()
    return Response(table_html)

print(del_user(), '!!!!!!!!!!!!!!!!!!!!!!!!')


@app.route('/table')
def table():
    return render_template('table.html')

@app.route('/window')
def window():
    return render_template('window.html')

@app.route('/test')
def ttest():
    return render_template('test.html')



if __name__ == '__main__':
    app.run(debug=True)
