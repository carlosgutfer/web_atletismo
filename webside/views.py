from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import  check_password_hash
from .models.bbdd import User_register
from . import db
from .database import querys_ddbb as qdb
from .estadillos import estadillo_sub16_masculino_al,estadillo_sub16_femenino_al
import csv
import os
from werkzeug.utils import secure_filename


views = Blueprint('views', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

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
                    return render_template("home.html", User_register=current_user, data = qdb.get_notes())
        else:
            if request.form.get('title'):
                qdb.insert_note(request.form.get('title'), request.form.get('textarea'), current_user.id)
            return render_template("home.html", User_register=current_user, data = qdb.get_notes() )
    elif request.method == 'GET' and current_user.is_active:
        return render_template("home.html", User_register=current_user, data = qdb.get_notes() )
    return render_template("login.html", User_register=current_user)


@views.route('/user_info', methods=['POST', 'GET'])
@login_required
def user_info():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template("user_info.html", User_register=current_user, fail = True)

        file = request.files['file']

        if file.filename == '':
            return render_template("user_info.html", User_register=current_user, fail = True)

        if file and allowed_file(file.filename) and  len(file.read()) < current_app.config['MAX_IMAGE_SIZE_BYTES']:
            filename = secure_filename(file.filename)
            filename = filename.replace('/', '_')
            file.seek(0)
            ruta = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            qdb.update_user(current_user, ruta)
            file.save(ruta)
            return render_template("user_info.html", User_register=current_user, fail = False, image = current_user.url_photo.split('\\')[-1])
    image = None
    if current_user.url_photo != None:
        image = current_user.url_photo.split('\\')[-1]
    return render_template("user_info.html", User_register=current_user, image = image)


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

@views.route('/estadillos', methods=['POST', 'GET'])
@login_required
def estadillos():
 with open(r'C:/WEB_ATLETISMO/club.csv', newline= '') as csvfile:
        copia = []
        spamreader = csv.reader(csvfile, delimiter=';')
        copia = [a for a in spamreader]
        copia[0] = [copia[0][0][3:]]
        with open('readme.txt', 'w') as f:
            for user in copia:
                f.write("\n=============" + user[0] +  "=============")
                marcas = qdb.get_marks_for_pop(user[0])
                print(user[0])
                if len(marcas) != 0:
                    estadillo_masc, max_masc, final_marks =estadillo_sub16_masculino_al(marcas)
                    nombres_apellidos = [[mark[2] + mark[3], mark[1].disciplina] for mark in estadillo_masc]
                    for key,value in final_marks.items():
                        f.write("\n" +str(key)) 
                        for marks in value:
                            nombre =  marks[2] + marks[3]
                            for x in nombres_apellidos:
                                if nombre  == x[0]:
                                    f.write("\n" +str(marks) + " -- " + x[1])
                                    break
                                elif x == nombres_apellidos[-1]:
                                    f.write("\n" +str(marks))   
                    f.write("\n==============estadillo=================")
                    for marcas_finales in estadillo_masc:
                        f.write('\n' + str(marcas_finales))
                    f.write('\n' + str(max_masc))
                try:
                        estadillo_fem,max_fem,final_marks =  estadillo_sub16_femenino_al(marcas)
                        nombres_apellidos = [[mark[2] + mark[3], mark[1].disciplina]for mark in estadillo_fem]
                        for key,value in final_marks.items():
                            f.write("\n" +str(key)) 
                            for marks in value:
                                nombre =  marks[2] + marks[3]
                                for x in nombres_apellidos:
                                    if nombre  == x[0]:
                                        f.write("\n" +str(marks) + " -- " + x[1])
                                        break
                                    elif x == nombres_apellidos[-1]:
                                        f.write("\n" +str(marks))   
                        f.write("\n==============estadillo=================")   
                        for marcas_finales in estadillo_fem:
                            f.write('\n'+ str (marcas_finales))
                        f.write('\n' + str(max_fem))
                        f.write("\n=======================================")
                except:
                    f.write("\n=============Fallo calculo femenino=============")
                   
        return render_template("estadillos.html", User_register=current_user)#, estadillo_fem = estadillo_fem, estadillo_masc = estadillo_masc, max_masc = max_masc, max_fem = max_fem)