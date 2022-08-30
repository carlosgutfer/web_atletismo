from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
import numpy as np
from werkzeug.security import generate_password_hash, check_password_hash

from .models.User import User_register, Marca, Technification, Notes
from . import db


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
                    data = db.session.query(User_register.name, Notes.texto, Notes.title ).select_from(Notes).join(User_register, User_register.id == Notes.user_id).all()      
                    return render_template("home.html", User_register=current_user, data = data)
                else:
                    flash('Incorrect password, try again.', category='error')
        else:
            if request.form.get('title'):
                title =  request.form.get('title')
                textarea =  request.form.get('textarea')
                note = Notes(title = title, texto =  textarea, user_id =  current_user.id)
                db.session.add(note)
                db.session.commit()
            data = db.session.query(User_register.name, Notes.texto, Notes.title ).select_from(Notes).join(User_register, User_register.id == Notes.user_id).all()      
            return render_template("home.html", User_register=current_user, data = data)
    return render_template("login.html", User_register=current_user)

@views.route('/insert_mark', methods=['POST', 'GET'])
@login_required
def insert_mark():
    if request.method == 'POST':
        sector = request.form.get('tipo_prueba')
        competition_date = request.form.get('sesion_date')
        if sector != 'Fondo / Medio Fondo':
            disciplina = request.form.get(sector)
        else:
            disciplina = request.form.get('FondoMedioFondo')
        marca = request.form.get('marca')
        if sector in ['Lanzamientos', 'Saltos']:
            nueva_marca = Marca(sector = sector, disciplina = disciplina, date = datetime.strptime(competition_date, '%Y-%m-%d').date(), meters = float(marca), user_id = current_user.id)
        else:
            nueva_marca = Marca(sector = sector, disciplina = disciplina, date = datetime.strptime(competition_date, '%Y-%m-%d').date(), time = datetime.strptime(marca, '%M:%S.%f').time(), user_id = current_user.id)
        db.session.add(nueva_marca)
        db.session.commit()
    return render_template("insert_mark.html", User_register=current_user)

@views.route('/view_all_marks', methods=['POST', 'GET'])
@login_required
def view_all_marks():
    if request.method == 'POST':
            id = request.form.get('cod_usuario')
            all_marks = Marca.query.filter_by(user_id = id).all()
            return render_template("view_all_marks.html", User_register=current_user, marks = all_marks)
    all_marks = Marca.query.filter_by(user_id = current_user.id).all()
    return render_template("view_all_marks.html", User_register=current_user, marks = all_marks)

@views.route('/view_marks_by_discipline', methods=['POST', 'GET'])
@login_required
def view_marks_by_discipline():
    if request.method == 'POST' and request.form.get('tipo_prueba') != 'SECTORES':
        if current_user.admin and request.form.get('cod_usuario') != '':
            id = request.form.get('cod_usuario')
        else:
            id = current_user.id
        if request.form.get('tipo_prueba') in ['Velocidad','Vallas']:
            all_marks =  Marca.query.with_entities(Marca.date, Marca.time).filter_by(user_id = id, disciplina = request.form.get(request.form.get('tipo_prueba'))).order_by(Marca.date.asc()).all()
            minimo = (np.amin(np.array([row[1] for row in all_marks]))).strftime("%H:%M:%S.%f")
            maximo = (np.amax(np.array([row[1] for row in all_marks]))).strftime("%H:%M:%S.%f")
            maxmin = [minimo[0:-4], maximo[0:-4]]
            date = [row[0].strftime("%d/%m/%Y") for row in all_marks]
            time = [row[1].strftime("%H:%M:%S.%f") for row in all_marks]
            return render_template("view_marks_by_discipline.html", User_register=current_user, date = date, time = time, tipo = 1, maxmin = maxmin)
        elif request.form.get('tipo_prueba') in ['Saltos', 'Lanzamientos']:
            all_marks =  Marca.query.with_entities(Marca.date, Marca.meters).filter_by(user_id = id, disciplina = request.form.get(request.form.get('tipo_prueba'))).order_by(Marca.date.asc()).all()
            date = [row[0].strftime("%d/%m/%Y") for row in all_marks]
            time = [row[1] for row in all_marks]
            return render_template("view_marks_by_discipline.html", User_register=current_user, date = date, time = time, tipo = 2, maxmin = 0)
        else:
            all_marks =  Marca.query.with_entities(Marca.date, Marca.time).filter_by(user_id = id, disciplina = request.form.get('FondoMedioFondo')).order_by(Marca.date.asc()).all()
            minimo = (np.amin(np.array([row[1] for row in all_marks]))).strftime("%H:%M:%S.%f")
            maximo = (np.amax(np.array([row[1] for row in all_marks]))).strftime("%H:%M:%S.%f")
            maxmin = [minimo[0:-4], maximo[0:-4]]
            if maxmin[0] == maxmin[1]:
                maxmin[1] = maxmin[0][0:-7] + str(int(maxmin[0][-7:-6]) + 1) + maxmin[0][5:]
            date = [row[0].strftime("%d/%m/%Y") for row in all_marks]
            time = [row[1].strftime("%H:%M:%S.%f") for row in all_marks]
            return render_template("view_marks_by_discipline.html", User_register=current_user, date = date, time = time, tipo = 3, maxmin= maxmin)
    else:
        return render_template("view_marks_by_discipline.html", User_register=current_user, tipo = 0)

@views.route('/delete_mark', methods=['POST', 'GET'])
@login_required
def delete_mark():
    all_marks = Marca.query.filter_by(user_id = current_user.id).all()
    if request.method == 'POST' and len(all_marks) != 0:
        id = int(request.form.get('tipo_prueba').split(' / ')[0])
        marca = Marca.query.filter_by(id=id).first()
        db.session.delete(marca)
        db.session.commit()
        return render_template("delete_marks.html", User_register=current_user, marks = all_marks)
    return render_template("delete_marks.html", User_register=current_user, marks = False)

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
        return render_template("sing_up.html", User_register=current_user)

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

@views.route('/insert_Technification', methods=['POST', 'GET'])
@login_required
def insert_Technification():
    all_user = User_register.query.all()
    if request.method == 'POST':
        id = int(request.form.get('user').split(' / ')[0])
        name_group = request.form.get('grupo_tecnificacion')
        week_day = request.form.get('dia_semana')
        new_tecnification = Technification(name_group = name_group, week_day = week_day, user_id = id)
        db.session.add(new_tecnification)
        db.session.commit()
        transaction = True
        return render_template("insert_tech_group.html", User_register=current_user, users = all_user, transaction = transaction)
    return render_template("insert_tech_group.html", User_register=current_user, users = all_user)

@views.route('/view_technification_groups', methods=['POST', 'GET'])
@login_required
def view_technification_groups():   
    data = db.session.query(User_register.name, User_register.surname, Technification.name_group, Technification.week_day).select_from(Technification).join(User_register, User_register.id == Technification.user_id).all()      
    return render_template("view_technification_groups.html", User_register = current_user , data = data)

@views.route('/view_filter_technification_group', methods=['POST', 'GET'])
@login_required
def view_filter_technification_group():
    if request.method == 'POST':
        data = db.session.query(User_register.name, User_register.surname).select_from(Technification).filter_by(name_group = request.form.get('grupo_tecnificacion'), week_day = request.form.get('dia_semana')).join(User_register, User_register.id == Technification.user_id).all()         
        return render_template("view_filter_technification_group.html", User_register = current_user, data = data, name_group = request.form.get('grupo_tecnificacion'), week_day = request.form.get('dia_semana'))
    return render_template("view_filter_technification_group.html", User_register = current_user )   

@views.route('/delete_technification_member', methods=['POST', 'GET'])
@login_required
def delete_technification_member():
    data = db.session.query(User_register.id, User_register.name, User_register.surname, Technification.name_group, Technification.week_day).select_from(Technification).join(User_register, User_register.id == Technification.user_id).all()      
    if request.method == 'POST':
       id = int(request.form.get('user').split(' - ')[0])
       group = Technification.query.filter_by(user_id=id).first()
       if group:
            db.session.delete(group)
            db.session.commit()
    return render_template("delete_technification_member.html",  User_register=current_user , all_user = data)
