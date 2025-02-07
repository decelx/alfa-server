# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask import request
from flask import Response
import psycopg2
from config import load_config
from urllib.parse import urlparse
from uuid import *
from gen_name import *
from credit_calc import Calculator
from model import User, Reference
from flask_sqlalchemy import SQLAlchemy

import log_app
import logging

config = load_config('postgresql_db')

logger = logging.getLogger(__name__)
logging.basicConfig(filename='app.log', level=logging.INFO)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:decel99@127.0.0.1:5432/postgres"

db = SQLAlchemy()
db.init_app(app)

with app.app_context():
    db.create_all()


def connect():
    """Функция возвращающая обЪект подключения к БД"""
    try:
        logger.info('обращение к БД')
        conn = psycopg2.connect(**config)
        return conn
    except Exception as err:
        logger.error(err)



def get_20(num: int = 1) -> list:
    """Функция возвращает список 20ти справок"""
    references = db.session.query(Reference.surname, Reference.name, Reference.father, Reference.reference, Reference.id, Reference.document).all()

    count = 0
    answer = []

    for ref in references:
        count += 1
        if ((num - 1) * 20) <= count <= (num * 20):
            ref_mod = Reference(*ref)
            answer.append(ref_mod)
    return answer


@app.route('/index', methods=['POST'])
def insertUser():
    """Добовляем пользывателей в БД"""
    if request.method == 'POST':
        surname_x = request.json['surname']
        name_x = request.json['name']
        father = request.json['father']
        reference = request.json['reference']
        docsType = request.json['docsType']
        id = uuid4()

        try:
            ref = Reference(surname_x, name_x, father, reference, id, docsType)
            db.session.add(ref)
            db.session.commit()

            return Response('done', status=200)
        except Exception as error:
            print(error)
            return Response('fail', status=500)


@app.route('/credit_calc', methods=["POST"])
def credit_calc():
    """Функция задает условия одобрения кредита и в случае совподение условий возврощает одобрение"""
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


@app.route('/gen_table/', methods=["POST"])
def gen_table():
    """вставляет данные в таблицу"""
    if request.method == 'POST':
        num = request.json['num']

        try:
            referenses = get_20(num)
            count = 1
            table_html = ""
            for ref in referenses:    #перейти от индексов к использыванию обьектов референс
                tr = f"""
                    <tr>
                        <th scope="row">{count}</th>
                        <td class="surname">{ref.surname}</td>   
                        <td class="name">{ref.name}</td>
                        <td class="father">{ref.father}</td>
                        <td class="ref">{ref.reference}</td>
                        <td class="doc">{ref.document}</td>
                        <td><button type="button" class="btn btn-danger btn-lg print-btn" data-toggle="modal" data-target="#staticBackdrop" style="background: #e80000;">Печать</button></td>
                    </tr>    
                """
                table_html += tr
                count += 1
            return Response(table_html, status=200)
        except Exception as error:                              # создать файл для логирования либо использывать готовые инструминты
            # print(error)
            return Response('fail', status=404)


@app.route('/del_user', methods=["POST"])
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
        # print(table_html)
    conn.close()
    return Response(table_html)

print(del_user(), '!!!!!!!!!!!!!!!!!!!!!!!!')


def delete_user(id):
    try:
        user_id = db.session.query(User).filter(User.id==id).delete()
        db.session.commit()
        a = 1 / 0
    except Exception as error:
        log_app.write_log(error)

    # list_id = []
    #
    # for i in user_id:
    #     list_id.append(i)

    return user_id


def file_error(error):
    try:
        with open('error.txt', 'w') as f:
            f.writelines(error)
    except:
        print("Ошибка работы с файлом")


####################################   роуты   ###################################
@app.route('/')
def index():
    """оброботчик загрузки стартовой страницы"""
    delete_user(5)
    return render_template('home.html')


@app.route('/application')
def test2():
    return render_template('application.html')


@app.route('/calculator')
def calculator():
    return render_template('calculator.html')


@app.route('/table')
def table():
    return render_template('table.html')


@app.route('/test')
def ttest():
    return render_template('test.html')

####################################   конец роуты   ###################################

if __name__ == '__main__':
    app.run(debug=True)
