import datetime
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .database import querys_ddbb as qdb

test = Blueprint('test', __name__)

@test.route('/view_all_test', methods=['POST', 'GET'])
@login_required
def view_all_test():
    if request.method == 'POST'and current_user.admin:
            ids = request.form.getlist('ids')
            return render_template("view_all_test_admin.html", User_register=current_user, test = qdb.get_all_test_admin(ids), all_user = qdb.get_all_user())
    elif request.method == 'GET'and current_user.admin:
            return render_template("view_all_test_admin.html", User_register=current_user, test = qdb.get_all_test_admin([current_user.id]), all_user = qdb.get_all_user())
    return render_template("view_all_test.html", User_register=current_user, marks = qdb.get_all_test(current_user.id))

@test.route('/insert_test', methods=['POST', 'GET'])
@login_required
def insert_test():
    if request.method == 'POST':
        qdb.insert_test(request.form.get('tipo_test'), request.form.get('sesion_date'),  request.form.get('repeticiones'), request.form.get('marca'), current_user.id)
    return render_template("insert_test.html", User_register=current_user)

@test.route('/view_test_filter', methods=['POST','GET'])
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
            labels = []
            for x in data:
                for y in x[0]:
                    labels.append(y)
            dates = [datetime.datetime.strptime(ts, "%d/%m/%Y") for ts in labels]
            dates.sort()
            sorteddates = [datetime.datetime.strftime(ts, "%d/%m/%Y") for ts in dates]
            return render_template("view_test_filter_admin.html", User_register=current_user,date = [x[0] for x in data], time = [x[1] for x in data], actual =  [x[2] for x in data], all_user = qdb.get_all_user(), names = [x[3][0] for x in data], labels = sorteddates)
    elif request.method == 'POST':
        data = qdb.get_mark_by_test(request.form.get('tipo_test'), id = current_user.id)
        if not data:
             return render_template("view_test_filter.html", User_register=current_user, date = [], time = [])
        return render_template("view_test_filter.html", User_register=current_user, date = data[0], time = data[1], actual = data[2])
    return render_template("view_test_filter.html", User_register=current_user, date = [], time = [])

@test.route('/delete_test', methods=['POST', 'GET'])
@login_required
def delete_test():
    all_test = qdb.get_all_test(current_user.id)
    if request.method == 'POST':
        id = int(request.form.get('tipo_test').split(' / ')[0])
        qdb.delete_test(id)
    if len(all_test) != 0:
        return render_template("delete_test.html", User_register=current_user, test = all_test)
    return render_template("delete_test.html", User_register=current_user, test = False)

