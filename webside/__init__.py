from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from datetime import timedelta

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'MdLr37P.'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
    db.init_app(app)

    from .views import  views
    from .marks import marks
    from .test import test
    from .technification import technification

    app.register_blueprint(technification, url_prefix= '/')
    app.register_blueprint(views, url_prefix= '/')
    app.register_blueprint(marks, url_prefix='/')
    app.register_blueprint(test, url_prefix='/')

    create_database(app)

   
    
    from .models.User import User_register

    login_manager = LoginManager()
    login_manager.login_view = 'views.home'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User_register.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
