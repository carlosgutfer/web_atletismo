from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import datetime
from .database import querys_ddbb as qdb

moods = Blueprint('moods', __name__)

@moods.route('/insert_mood', methods=['POST', 'GET'])
def insert_mood():
    if request.method == 'POST':
        year = int(request.form.get('sesion_date')[:4])
        month = int(request.form.get('sesion_date')[5:7])
        day = int(request.form.get('sesion_date')[8:])
        week = datetime.date(year, month, day).isocalendar()[1]
        qdb.insert_mood(request.form.get('sesion_date'),  int(request.form.get('mood_note')), week, current_user.id)
    return render_template("insert_mood.html", User_register=current_user)


@moods.route('/view_mood', methods=['GET'])
def view_mood():
    moods = qdb.view_all_moods(current_user.id)
    all_moods = []
    semana = 0
    aux = []
    for x in moods:
        if (x.week != semana and  semana == 0):
            semana = x.week
            aux.append(x)
        elif (x.week == semana):
            aux.append(x)
        else:
            all_moods.append(aux)
            aux = []
            aux.append(x)
            semana = x.week
        if (x == moods[-1]):
            all_moods.append(aux)
    media = []
    for moods in all_moods:
        aux = 0
        for notes in moods:
            aux += notes.note
        aux /= len(moods)
        media.append(aux)
    fecha = []
    notes = []
    names = []
    for x in all_moods:
        aux1 = []
        aux2 = []
        for y in x:
            aux1.append((y.date).strftime("%d/%m/%Y"))
            aux2.append(y.note)
            if str(y.week) not in names:
                names.append(str(y.week))
        fecha.append(aux1)
        notes.append(aux2)
        dias_semana = []
        for weeks in all_moods:
            aux = [] 
            for days in weeks: 
                aux.append(days.date.weekday())
            dias_semana.append(aux)         
    return render_template("view_all_mood.html", 
                            User_register=current_user, 
                            all_moods = all_moods, 
                            media = media, 
                            notes = notes,
                            fecha = fecha,
                            names = names,
                            dias_semana = dias_semana,
                            i = len(all_moods))