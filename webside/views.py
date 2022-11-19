from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import  check_password_hash
from .models.User import User_register
from . import db
from .database import querys_ddbb as qdb

views = Blueprint('views', __name__)


@views.route('/', methods=['POST','GET'])
def home():
    if request.method == 'POST':
        user_cod = request.form.get('user_cod')
        password = request.form.get('password')
        user = User_register.query.filter_by(id=user_cod).first()
        if not current_user.is_active:
            if user:
                if check_password_hash(user.password, password):
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    session.permanent = True
                    return render_template("home.html", User_register=current_user, data = qdb.get_notes())
        else:
            if request.form.get('title'):
                qdb.insert_note(request.form.get('title'), request.form.get('textarea'), current_user.id)
            return render_template("home.html", User_register=current_user, data = qdb.get_notes() )
    elif request.method == 'GET' and current_user.is_active:
        return render_template("home.html", User_register=current_user, data = qdb.get_notes() )
    return render_template("login.html", User_register=current_user)

@views.route('/sing_up', methods=['POST', 'GET'])
@login_required
def sign_up():
    if request.method == 'POST':
        qdb.insert_user(request.form.get('firstName'), request.form.get('password'), request.form.get('administrador'), request.form.get('surname'))
        return render_template("sing_up.html", User_register=current_user)
    return render_template("sing_up.html", User_register=current_user)

@views.route('/change_pass', methods=['POST', 'GET'])
@login_required
def change_pass():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        password1 = request.form.get('new_password1')
        password2 = request.form.get('new_password2')
        if password1 == password2:
            if check_password_hash(current_user.password, old_password):
                qdb.update_password(current_user, password1)
                return render_template("change_pass.html", User_register=current_user)
    return render_template("change_pass.html", User_register=current_user)

@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@views.route('/view_all')
@login_required
def view_all():
    return render_template("view_all.html",  User_register=current_user , all_user= qdb.get_all_user())

@views.route('/delete_user', methods=['POST', 'GET'])
@login_required
def delete_user():
    if request.method == 'POST':
        cod_user =request.form.get('cod_user')
        name = request.form.get('firstName')
        user = User_register.query.filter_by(id=cod_user, name = name).first()
        password = request.form.get('password')
        if user:
             if check_password_hash(current_user.password, password):
                db.session.delete(user)
                db.session.commit()
                return render_template("delete_user.html", User_register=current_user, eliminado = True)

    return render_template("delete_user.html", User_register=current_user, eliminado = False)

@views.route('/reset_pass', methods=['POST', 'GET'])
@login_required
def reset_pass():
    if request.method == 'POST':
        cod_user = request.form.get('user_id')
        name = request.form.get('user_name')
        user = User_register.query.filter_by(id=cod_user, name = name).first()
        password = 'cal2022'
        if user:
            qdb.update_password(user, password)
            return render_template("reset_pass.html", User_register=current_user, cambiada = True)
    return render_template("reset_pass.html", User_register=current_user)
