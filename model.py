from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    """"""
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    password = db.Column(db.Text())
    email = db.Column(db.Text())

    def __init__(self, id, password, email):
        self.id = id
        self.password = password
        self.email = email

    def to_dict(self):
        return {
            "email": self.email,
            "password": self.password
        }



class Reference(db.Model):
    __tablename__ = "reference"
    surname = db.Column(db.Text())
    name = db.Column(db.Text())
    father = db.Column(db.Text())
    reference = db.Column(db.Text())
    id = db.Column(db.Text(), primary_key=True, nullable=False)
    document = db.Column(db.Text())

    def __init__(self, surname, name, father, reference, id, document):
        self.surname = surname
        self.name = name
        self.father = father
        self.reference = reference
        self.id = id
        self.document = document

    def to_dict(self):
        return {
            "id": self.id,
            "reference": self.reference
        }
