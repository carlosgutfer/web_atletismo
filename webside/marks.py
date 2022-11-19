import datetime
from flask import Blueprint, render_template, request
from flask_login import  login_required, current_user
from .database import querys_ddbb as qdb

marks = Blueprint('marks', __name__)

@marks.route('/insert_mark', methods=['POST', 'GET'])
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

@marks.route('/view_all_marks', methods=['POST', 'GET'])
@login_required
def view_all_marks():
    if request.method == 'POST' and current_user.admin:
            ids = []
            if 'seleccion a todos' not in request.form.getlist('ids'):
                ids = request.form.getlist('ids')
            return render_template("view_all_marks_admin.html", User_register=current_user, marks = qdb.get_all_marks_admin(ids),all_user = qdb.get_all_user())
    elif request.method == 'GET'and current_user.admin:
        return render_template("view_all_marks_admin.html", User_register=current_user, marks = qdb.get_all_marks_admin([current_user.id]), all_user = qdb.get_all_user())
    return render_template("view_all_marks.html", User_register=current_user, marks = qdb.get_all_marks(current_user.id))

@marks.route('/view_marks_by_discipline', methods=['POST', 'GET'])
@login_required
def view_marks_by_discipline():
    if request.method == 'GET' and current_user.admin:
        return render_template("view_marks_by_discipline_admin.html", User_register=current_user, tipo = 0, all_user = qdb.get_all_user())
    if request.method == 'POST' and current_user.admin:
        if 'seleccion a todos' not in request.form.getlist('ids'):
            ids = request.form.getlist('ids')
        else:
            ids =[id[0] for id in  qdb.get_all_user()]
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
            labels = []
            for x in all_marks:
                for y in x[0]:
                    labels.append(y)
            dates = [datetime.datetime.strptime(ts, "%d/%m/%Y") for ts in labels]
            dates.sort()
            sorteddates = [datetime.datetime.strftime(ts, "%d/%m/%Y") for ts in dates]
            if tipo_prueba  not in ['Lanzamientos', 'Saltos']:
                return render_template("view_marks_by_discipline_admin.html", 
                User_register=current_user,
                date = [x[0] for x in all_marks], 
                time = [x[1] for x in all_marks], 
                tipo = all_marks[0][2],
                maxmin = [min([x[3][0] for x in all_marks]), max([x[3][1] for x in all_marks])], 
                names = [x[4][0] for x in all_marks],
                all_user = qdb.get_all_user(),
                labels = sorteddates )
            else:
                return render_template("view_marks_by_discipline_admin.html", 
                User_register=current_user,
                date = [x[0] for x in all_marks], 
                time = [x[1] for x in all_marks], 
                tipo = all_marks[0][2],
                maxmin = all_marks[0][3], 
                names = [x[4][0] for x in all_marks],
                all_user = qdb.get_all_user(),
                labels = sorteddates )
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

@marks.route('/delete_mark', methods=['POST', 'GET'])
@login_required
def delete_mark():
    all_marks = qdb.get_all_marks(current_user.id)
    if request.method == 'POST':
        id = int(request.form.get('tipo_prueba').split(' / ')[0])
        qdb.delete_mark(id)
    if len(all_marks) != 0:
        return render_template("delete_marks.html", User_register=current_user, marks = all_marks)
    return render_template("delete_marks.html", User_register=current_user, marks = False)