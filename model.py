from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
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

