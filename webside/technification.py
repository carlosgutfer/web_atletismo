from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models.User import User_register, Technification
from . import db
from .database import querys_ddbb as qdb

technification = Blueprint('technification', __name__)


@technification.route('/insert_Technification', methods=['POST', 'GET'])
@login_required
def insert_Technification():
    all_user = User_register.query.all()
    if request.method == 'POST':
        transaction = qdb.insert_technification(request.form.get('user'), request.form.get('grupo_tecnificacion'), request.form.get('dia_semana'))
        return render_template("insert_tech_group.html", User_register=current_user, users = all_user, transaction = transaction)
    return render_template("insert_tech_group.html", User_register=current_user, users = all_user)

@technification.route('/view_technification_groups', methods=['POST', 'GET'])
@login_required
def view_technification_groups():   
    data = db.session.query(User_register.name, User_register.surname, Technification.name_group, Technification.week_day).select_from(Technification).join(User_register, User_register.id == Technification.user_id).all()      
    return render_template("view_technification_groups.html", User_register = current_user , data = data)

@technification.route('/view_filter_technification_group', methods=['POST', 'GET'])
@login_required
def view_filter_technification_group():
    if request.method == 'POST':
        data = db.session.query(User_register.name, User_register.surname).select_from(Technification).filter_by(name_group = request.form.get('grupo_tecnificacion'), week_day = request.form.get('dia_semana')).join(User_register, User_register.id == Technification.user_id).all()         
        return render_template("view_filter_technification_group.html", User_register = current_user, data = data, name_group = request.form.get('grupo_tecnificacion'), week_day = request.form.get('dia_semana'))
    return render_template("view_filter_technification_group.html", User_register = current_user )   

@technification.route('/delete_technification_member', methods=['POST', 'GET'])
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


