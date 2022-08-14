from .. import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User_register(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    surname = db.Column(db.String(150))
    admin = db.Column(db.Boolean)
    marcas = db.relationship('Marca')
    test = db.relationship('Test')

class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    discipline = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user_register.id'))

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user_register.id'))