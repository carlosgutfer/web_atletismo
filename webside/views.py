from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models.User import User_register 
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

views = Blueprint('views', __name__)

@views.route('/', methods=['POST','GET'])
def home():
    if request.method == 'POST':
        user_cod = request.form.get('user_cod')
        password = request.form.get('password')

        user = User_register.query.filter_by(id=user_cod).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return render_template("comprobar__mm__gap.html", User_register=current_user)
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", User_register=current_user)


@views.route('/insert_mark', methods=['POST', 'GET'])
@login_required
def mm_gap():
    return render_template("insert_mark.html", User_register=current_user)


@views.route('/px_gap', methods=['POST', 'GET'])
@login_required
def px_gap():
    return render_template("comprobar__px_gap.html", User_register=current_user)

@views.route('/sing_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        name = request.form.get('firstName')
        password = request.form.get('password')
        if request.form.get('administrador'):
            admin = True
        else:
            admin = False
        surname = request.form.get('surname')
        new_user = User_register(name=name, password=generate_password_hash(password, method='sha256'), admin = admin, surname=surname)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        return redirect(url_for('views.home'))

    return render_template("sing_up.html", User_register=current_user)


@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@views.route('/view_all')
@login_required
def view_all():
    all_user = User_register.query.all()
    return render_template("view_all.html",  User_register=current_user , all_user=all_user )

@views.route('/delete_user', methods=['POST', 'GET'])
@login_required
def delete_user():
    if request.method == 'POST':
        cod_user =request.form.get('cod_user')
        name = request.form.get('firstName')
        password = request.form.get('password')
        user = User_register.query.filter_by(id=cod_user, name = name).first()
        if user:
             if check_password_hash(current_user.password, password):
                db.session.delete(user)
                db.session.commit()
                return render_template("delete_user.html", User_register=current_user, eliminado = True)

    return render_template("delete_user.html", User_register=current_user, eliminado = False)


