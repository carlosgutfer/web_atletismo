import datetime
from flask import Blueprint, render_template, request
from flask_login import  login_required, current_user
from .database import querys_ddbb as qdb

assitant = Blueprint('assitant', __name__)

@assitant.route('/insert_asitant', methods=['GET', 'POST'])
def inser_assitant():
    all_user = qdb.get_all_user()
    if request.method == 'POST':
        return render_template('assistan.html', User_register=current_user, all_user = all_user)
    return render_template('assistan.html', User_register=current_user, all_user = all_user)