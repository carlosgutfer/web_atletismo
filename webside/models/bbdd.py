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
    test = db.relationship('test')
    group = db.relationship('Technification')


class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sector = db.Column(db.String(10000))
    disciplina = db.Column(db.String(10000))
    date = db.Column(db.Date)
    meters = db.Column(db.Float)
    time = db.Column(db.Time)
    user_id = db.Column(db.Integer, db.ForeignKey('user_register.id'))

class test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(10000))
    repeticiones = db.Column(db.Integer)
    mark = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user_register.id'))

class Technification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_group = db.Column(db.String(10000))
    week_day = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user_register.id'))

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10000))
    texto = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user_register.id'))

class  Mood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    note = db.Column(db.Integer)
    week = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user_register.id'))

