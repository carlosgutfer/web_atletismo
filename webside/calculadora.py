from flask import Blueprint, render_template, request
from flask_login import  login_required, current_user

calculate = Blueprint('calculate', __name__)

@calculate.route('/calculate', methods=['POST', 'GET'])
@login_required
def calculate_view():
    if request.method == 'POST':
        type = request.form.get('tipo')
        min = request.form.get('minutos')
        seg = request.form.get('segundos')
        dec = request.form.get('decimas')
        mark = request.form.get('current_mark')
        goal_mark = request.form.get('goal_mark')
        total_time = int(min) * 60 + int(seg) + int(dec) // 10
        if type == 'Porcentaje':
            goal_mark = total_time * float(goal_mark)
        else:
            goal_mark = int(goal_mark)
            mark = total_time / int(mark)
            goal_mark *= mark
        final_min = goal_mark // 60
        final_seg = goal_mark % 60
        return render_template("calculate.html", User_register=current_user, min = int(final_min), seg = final_seg)
    return render_template("calculate.html", User_register=current_user)