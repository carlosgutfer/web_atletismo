from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import  check_password_hash
from .models.User import User_register, Technification
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

@views.route('/insert_mark', methods=['POST', 'GET'])
@login_required
def insert_mark():
    if request.method == 'POST':
        sector = request.form.get('tipo_prueba')
        if sector != 'Fondo / Medio Fondo':
            disciplina = request.form.get(sector)
        else:
            disciplina = request.form.get('FondoMedioFondo')
        qdb.insert_mark(request.form.get('tipo_prueba'),  request.form.get('sesion_date'), request.form.get('marca'), disciplina, current_user.id)
    return render_template("insert_mark.html", User_register=current_user)

@views.route('/view_all_marks', methods=['POST', 'GET'])
@login_required
def view_all_marks():
    if request.method == 'POST' and current_user.admin:
            ids = request.form.getlist('ids')
            return render_template("view_all_marks_admin.html", User_register=current_user, marks = qdb.get_all_marks_admin(ids),all_user = qdb.get_all_user())
    elif request.method == 'GET'and current_user.admin:
        return render_template("view_all_marks_admin.html", User_register=current_user, marks = qdb.get_all_marks_admin([current_user.id]), all_user = qdb.get_all_user())
    return render_template("view_all_marks.html", User_register=current_user, marks = qdb.get_all_marks(current_user.id))

@views.route('/view_marks_by_discipline', methods=['POST', 'GET'])
@login_required
def view_marks_by_discipline():
    if request.method == 'GET' and current_user.admin:
        return render_template("view_marks_by_discipline_admin.html", User_register=current_user, tipo = 0, all_user = qdb.get_all_user())
    if request.method == 'POST' and current_user.admin:
        ids = request.form.getlist('ids')
        tipo_prueba = request.form.get('tipo_prueba')
        if tipo_prueba != 'SECTORES':
            disciplina = request.form.get(tipo_prueba)
            all_marks = []
            if tipo_prueba in ['Velocidad','Vallas', 'Saltos', 'Lanzamientos']:
                    for id in ids:
                        answer = qdb.get_marks_by_discipline_admin(tipo_prueba, disciplina, id)
                        if answer:
                            if len(answer[0]) > 0 :
                                all_marks.append(answer) 
            else:
                for id in ids:
                    answer = qdb.get_marks_by_discipline_admin('FondoMedioFondo', request.form.get('FondoMedioFondo'), id)
                    if  answer:
                        if len(answer[0]) > 0 :
                                all_marks.append(answer)  
            if len(all_marks) == 0:
                 return render_template("view_marks_by_discipline_admin.html", User_register=current_user, tipo = 0, all_user = qdb.get_all_user())
            return render_template("view_marks_by_discipline_admin.html", User_register=current_user, date = [x[0] for x in all_marks], time = [x[1] for x in all_marks], tipo = all_marks[0][2], maxmin = all_marks[0][3], names = [x[4][0] for x in all_marks], all_user = qdb.get_all_user())
        return render_template("view_marks_by_discipline_admin.html", User_register=current_user, tipo = 0, all_user = qdb.get_all_user())
    elif request.method == 'POST':
        id = current_user.id
        tipo_prueba = request.form.get('tipo_prueba')
        if tipo_prueba != 'SECTORES':
            disciplina = request.form.get(tipo_prueba)
            if tipo_prueba in ['Velocidad','Vallas', 'Saltos', 'Lanzamientos']:
                all_marks = qdb.get_marks_by_discipline(tipo_prueba, disciplina, id)
            else:
                all_marks = qdb.get_marks_by_discipline('FondoMedioFondo', request.form.get('FondoMedioFondo'), id) 
                disciplina = request.form.get('FondoMedioFondo')
            if all_marks == False:
                    return render_template("view_marks_by_discipline.html", User_register=current_user, tipo = 0)
            return render_template("view_marks_by_discipline.html", User_register=current_user, date = all_marks[0], time = all_marks[1], tipo = all_marks[2], maxmin = all_marks[3],disciplina = disciplina )
    
    return render_template("view_marks_by_discipline.html", User_register=current_user, tipo = 0)


@views.route('/delete_mark', methods=['POST', 'GET'])
@login_required
def delete_mark():
    all_marks = qdb.get_all_marks(current_user.id)
    if request.method == 'POST':
        id = int(request.form.get('tipo_prueba').split(' / ')[0])
        qdb.delete_mark(id)
    if len(all_marks) != 0:
        return render_template("delete_marks.html", User_register=current_user, marks = all_marks)
    return render_template("delete_marks.html", User_register=current_user, marks = False)

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

@views.route('/insert_test', methods=['POST', 'GET'])
@login_required
def insert_test():
    if request.method == 'POST':
        qdb.insert_test(request.form.get('tipo_test'), request.form.get('sesion_date'),  request.form.get('repeticiones'), request.form.get('marca'), current_user.id)
    return render_template("insert_test.html", User_register=current_user)

@views.route('/view_all_test', methods=['POST', 'GET'])
@login_required
def view_all_test():
    if request.method == 'POST'and current_user.admin:
            ids = request.form.getlist('ids')
            return render_template("view_all_test_admin.html", User_register=current_user, test = qdb.get_all_test_admin(ids), all_user = qdb.get_all_user())
    elif request.method == 'GET'and current_user.admin:
            return render_template("view_all_test_admin.html", User_register=current_user, test = qdb.get_all_test_admin([current_user.id]), all_user = qdb.get_all_user())
    return render_template("view_all_test.html", User_register=current_user, marks = qdb.get_all_test(current_user.id))

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
        transaction = qdb.insert_technification(request.form.get('user'), request.form.get('grupo_tecnificacion'), request.form.get('dia_semana'))
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

@views.route('/view_test_filter', methods=['POST','GET'])
@login_required
def view_test_filter():
    if request.method == 'GET' and current_user.admin:
            return render_template("view_test_filter_admin.html", User_register=current_user, all_user = qdb.get_all_user())
    elif request.method == 'POST' and current_user.admin:
            data = []
            ids = request.form.getlist('ids')
            for id in ids:
                answer = qdb.get_mark_by_test(request.form.get('tipo_test'), id)
                if  answer:
                    data.append(answer)
            if not data:
                return render_template("view_test_filter_admin.html", User_register=current_user, all_user = qdb.get_all_user())
            return render_template("view_test_filter_admin.html", User_register=current_user,date = [x[0] for x in data], time = [x[1] for x in data], actual =  [x[2] for x in data], all_user = qdb.get_all_user())
    elif request.method == 'POST':
        data = qdb.get_mark_by_test(request.form.get('tipo_test'), id = current_user.id)
        if not data:
             return render_template("view_test_filter.html", User_register=current_user, date = [], time = [])
        return render_template("view_test_filter.html", User_register=current_user, date = data[0], time = data[1], actual = data[2])
    return render_template("view_test_filter.html", User_register=current_user, date = [], time = [])

@views.route('/delete_test', methods=['POST', 'GET'])
@login_required
def delete_test():
    all_test = qdb.get_all_test(current_user.id)
    if request.method == 'POST':
        id = int(request.form.get('tipo_test').split(' / ')[0])
        qdb.delete_test(id)
    if len(all_test) != 0:
        return render_template("delete_test.html", User_register=current_user, test = all_test)
    return render_template("delete_test.html", User_register=current_user, test = False)