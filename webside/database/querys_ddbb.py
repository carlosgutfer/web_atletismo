import hashlib
from datetime import datetime
import numpy as np
from werkzeug.security import generate_password_hash

from ..models.User import Marca, User_register, test, Technification, Notes
from .. import db 
from sqlalchemy import or_

def calculate_rm(max):
    rm = []
    rm.append(round(max))
    rm.append(round(max * 0.95))
    rm.append(round(max * 0.90))
    rm.append(round(max * 0.86))
    rm.append(round(max * 0.82))
    rm.append(round(max * 0.78))
    rm.append(round(max * 0.74))
    rm.append(round(max * 0.70))
    rm.append(round(max * 0.65))
    rm.append(round(max * 0.61))
    return rm

"""
    Methods for mark table

        --> Insert
        --> Get_all
        --> Get filter
        --> delete mark
"""
def insert_mark(sector, competition_date, marca, disciplina, id):
    '''
        def
                Insert mark on mark table
        Input  
                sector --> str\n
                competition_date -->  str\n
                marca --> str\n
                disciplina -->  str\n
                id --> int\n
        Output 
                true --> succesfull\n
                false --> something wrong \n
    
    '''
    try:
        if sector in ['Lanzamientos', 'Saltos']:
            nueva_marca = Marca(sector = sector, disciplina = disciplina, date = datetime.strptime(competition_date, '%Y-%m-%d').date(), meters = float(marca), user_id = id)
        else:
            nueva_marca = Marca(sector = sector, disciplina = disciplina, date = datetime.strptime(competition_date, '%Y-%m-%d').date(), time = datetime.strptime(marca, '%M:%S.%f').time(), user_id = id)
        db.session.add(nueva_marca)
        db.session.commit()
        return True
    except:
        return False

def get_all_marks(id):
    '''
        def 
            Select all register for one user on Marks table
        INPUT
            ID --> INT
        OUTPUT 
            array --> succesfull\n
            false --> something wrong
    '''
    try:
        all_marks = Marca.query.filter_by(user_id = id).all()
        return all_marks
    except:
        return False


def get_all_marks_admin(ids):
    '''
        def 
            Select all register for one user on Marks table
        INPUT
            ID --> INT
        OUTPUT 
            array --> succesfull\n
            false --> something wrong
    '''
    try:
        all_marks = db.session.query(User_register.name, User_register.surname, Marca).select_from(Marca).join(User_register, User_register.id == Marca.user_id).filter(or_(*[Marca.user_id.like(id) for id in ids])).all()
        return all_marks
    except:
        return False

def get_marks_by_discipline( tipo_prueba, disciplina, id):
    '''
        def
            Return * marks from an user and a discipline from marks table
        
        INPUT
            ID --> INT\n
            TIPO_PRUEBA --> STR\n
            DISCIPLINA --> STR\n
        
        OUTPUT 
             ARRAY --> SUCCESFULL\n
             FALSE --> something wrong
    '''
    try:
        if tipo_prueba in ['Velocidad','Vallas']:
            all_marks =  Marca.query.with_entities(Marca.date, Marca.time).filter_by(user_id = id, disciplina = disciplina).order_by(Marca.date.asc()).all()
            minimo = (np.amin(np.array([row[1] for row in all_marks]))).strftime("%H:%M:%S.%f")
            maximo = (np.amax(np.array([row[1] for row in all_marks]))).strftime("%H:%M:%S.%f")
            maxmin = [minimo[0:-4], maximo[0:-4]]
            date = [row[0].strftime("%d/%m/%Y") for row in all_marks]
            time = [row[1].strftime("%H:%M:%S.%f") for row in all_marks]
            return [date, time, 1, maxmin]
        elif tipo_prueba in ['Saltos', 'Lanzamientos']:
            all_marks =  Marca.query.with_entities(Marca.date, Marca.meters).filter_by(user_id = id, disciplina = disciplina).order_by(Marca.date.asc()).all()
            date = [row[0].strftime("%d/%m/%Y") for row in all_marks]
            time = [row[1] for row in all_marks]
            return [date, time, 2, 0]
        else:
            all_marks =  Marca.query.with_entities(Marca.date, Marca.time).filter_by(user_id = id, disciplina = disciplina).order_by(Marca.date.asc()).all()
            minimo = (np.amin(np.array([row[1] for row in all_marks]))).strftime("%H:%M:%S.%f")
            maximo = (np.amax(np.array([row[1] for row in all_marks]))).strftime("%H:%M:%S.%f")
            maxmin = [minimo[0:-4], maximo[0:-4]]
            if maxmin[0] == maxmin[1]:
                maxmin[1] = maxmin[0][0:-7] + str(int(maxmin[0][-7:-6]) + 1) + maxmin[0][5:]
            date = [row[0].strftime("%d/%m/%Y") for row in all_marks]
            time = [row[1].strftime("%H:%M:%S.%f") for row in all_marks]
            return [date, time, 3, maxmin]
    except:
        return False

def delete_mark(id):
    ''' 
        def
            Delete mark from table mark
        INPUT
            ID --> INT
        OUTPUT 
            TRUE --> SUCCESFULL\n
            FALSE --> SOMETHING IS WRONG
    '''
    try:
        marca = Marca.query.filter_by(id=id).first()
        db.session.delete(marca)
        db.session.commit()
        return True
    except:
        return False

"""
    Methods for User table

        --> Insert
"""
def insert_user(name, password, admin, surname):
    '''
        def 
            Insert new user 
        INPUT
            NAME --> STRING\n
            PASSWORD --> STRING\n
            ADMIN --> BOOL\n
            SURNAME --> STRING\n
        OUTPUT
            TRUE --> SUCCESFULL\n
            FALSE --> SOMETHING GO WRONG
    '''
    try:
        if admin is not None:
            admin = True
        else:
            admin = False
        new_user = User_register(name=name, password=generate_password_hash(password, method='sha256'), admin = admin, surname=surname)
        db.session.add(new_user)
        db.session.commit()
        return True
    except:
        return False

def update_password(usuario, password):
    setattr(usuario, 'password',generate_password_hash(password, method='sha256'))
    db.session.commit()

"""
    Technification group 
        --> Insert
"""
def insert_technification(user, name_group, week_day):
    '''
        def 
            Insert new record on technification table
        INPUT
            USER --> STR\n
            NAME_GROUP --> STR\n
            WEEK_DAY --> STR\n
        OUTPUT
            TRUE --> SUCCESFULL\n
            FALSE --> SOMETHING IS WRONG
        
    '''
    try:
        id = int(user.split(' / ')[0])
        new_tecnification = Technification(name_group = name_group, week_day = week_day, user_id = id)
        db.session.add(new_tecnification)
        db.session.commit()
        return True
    except:
        return False

def get_all_test(id):
    '''
        def 
            Select all register for one user on test table
        INPUT
            ID --> INT
        OUTPUT 
            array --> succesfull\n
            false --> something wrong
    '''
    try:
        all_test = test.query.filter_by(user_id = id).all()
        return all_test
    except:
        return False

def delete_test(id):
    ''' 
        def
            Delete record from table test
        INPUT
            ID --> INT
        OUTPUT 
            TRUE --> SUCCESFULL\n
            FALSE --> SOMETHING IS WRONG
    '''
    try:
        test_select = test.query.filter_by(id=id).first()
        db.session.delete(test_select)
        db.session.commit()
        return True
    except:
        return False


"""
    Methods for mark table

        --> Insert
        --> Get filter 
        --> Get all 
        --> delete test
"""
def insert_test(tipo_test, test_date, repeticiones, marca, id):
    '''
        def
            Insert new record on test table
        INPUT
            TIPO_TEST --> STR\n
            TEST_DATE --> STR\n
            REPETICIONES --> STR\n
            MARCA --> FLOAT\n
            ID --> INT\n
        OUTPUT
            TRUE --> SUCCESFULL\n
            FALSE --> SOMETHING IS WRONG
    '''
    try:
        nuevo_test = test(test_name = tipo_test, repeticiones = int(repeticiones), mark = marca, date = datetime.strptime(test_date, '%Y-%m-%d').date(), user_id = id)
        db.session.add(nuevo_test)
        db.session.commit()
        return True
    except:
        return False

def get_mark_by_test(tipo_test, id):
    '''
        def 
            Get all marks by test and return all mark and the max 
        INPUT
            TIPO_TEST --> STR\n
            ID --> INT\n
        OUTPUT
            RETURN ARRAY OF ARRAYS --> SUCCESFULL\n
            FALSE --> SOMETHING IS WRONG
    '''
    try:
        all_marks =  test.query.with_entities(test.date, test.mark, test.repeticiones).filter_by(user_id = id, test_name = tipo_test).order_by(test.date.asc()).all()
        date = [row[0].strftime("%d/%m/%Y") for row in all_marks]
        time = [(row[1] / (1.0278 - 0.0278 * row[2])) for row in all_marks]
        actual = calculate_rm(time[-1])
        return [date, time, actual]
    except:
        return False

def get_notes():
    return db.session.query(User_register.name, Notes.texto, Notes.title ).select_from(Notes).join(User_register, User_register.id == Notes.user_id).all()

def insert_note(title, textarea, id):
    '''
        def
            Insert new record on note table
        INPUT
            TITLE --> STR\n
            TEXTAREA --> STR\n
            ID --> INT\n
        OUTPUT
            TRUE --> SUCCESFULL\n
            FALSE --> SOMETHING IS WRONG
    '''
    try:
        note = Notes(title = title, texto =  textarea, user_id =  id)
        db.session.add(note)
        db.session.commit()
        return True
    except:
        return False
