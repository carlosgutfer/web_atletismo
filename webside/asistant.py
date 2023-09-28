from datetime import datetime
from flask import Blueprint, render_template, request
from flask_login import  login_required, current_user
from .database import querys_ddbb as qdb

assitant = Blueprint('assitant', __name__)

@assitant.route('/insert_asitant', methods=['GET', 'POST'])
def inser_assitant():
    all_user = qdb.get_all_user()
    if request.method == 'POST':
        if 'sesion_date' in request.form and len(request.form.keys()) > 1:
            try:
                fecha = request.form.get('sesion_date')
                fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
                week_day = fecha_obj.strftime('%A')
                year = int(fecha_obj.year)
                number_week = int(fecha_obj.strftime('%W'))
                ids = request.form.keys()
                qdb.insert_assist(ids, week_day, year, number_week)
            except:
                pass
    return render_template('assistan.html', User_register=current_user, all_user = all_user, tipo = 'insert')

@assitant.route('/view_assitant', methods=['GET', 'POST'])
def view_assitant():
    all_user = qdb.get_all_user()
    if request.method == 'POST':
        if 'sesion_date' in request.form:
            fecha = request.form.get('sesion_date')
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
            year = int(fecha_obj.year)
            number_week = int(fecha_obj.strftime('%W'))
            all_asist =  qdb.count_same_user_id_asist_by_week_and_year(number_week,year)
            return render_template('assistan.html', User_register = current_user, all_user = all_asist, tipo = 'view')
    return render_template('assistan.html', User_register=current_user, all_user = all_user, tipo = 'view')