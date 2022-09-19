import hashlib
from datetime import datetime
import numpy as np
from werkzeug.security import generate_password_hash
from collections import Counter
from ..models.User import Marca, User_register, test, Technification, Notes, test
from .. import db 
from sqlalchemy import or_
import csv

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


def get_marks_by_discipline_admin( tipo_prueba, disciplina, id):
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
            all_marks = db.session.query(Marca.date, Marca.time, User_register.name, User_register.surname).select_from(Marca).filter_by( disciplina = disciplina, user_id = id).join(User_register, User_register.id == Marca.user_id).order_by(Marca.date.asc()).all()            
            user = np.unique([row[2] + " " + row[3] for row in all_marks])
            minimo = (np.amin(np.array([row[1] for row in all_marks]))).strftime("%H:%M:%S.%f")
            maximo = (np.amax(np.array([row[1] for row in all_marks]))).strftime("%H:%M:%S.%f")
            maxmin = [minimo[0:-4], maximo[0:-4]]
            date = [row[0].strftime("%d/%m/%Y") for row in all_marks]
            time = [row[1].strftime("%H:%M:%S.%f") for row in all_marks]
            return [date, time, 1, maxmin, user]
        elif tipo_prueba in ['Saltos', 'Lanzamientos']:
            all_marks = db.session.query(Marca.date, Marca.meters, User_register.name, User_register.surname).select_from(Marca).filter_by( disciplina = disciplina, user_id = id).join(User_register, User_register.id == Marca.user_id).order_by(Marca.date.asc()).all()               
            user = np.unique([row[2] + " " + row[3] for row in all_marks])
            date = [row[0].strftime("%d/%m/%Y") for row in all_marks]
            time = [row[1] for row in all_marks]
            return [date, time, 2, 0, user]
        else:
            all_marks = db.session.query(Marca.date, Marca.time, User_register.name, User_register.surname).select_from(Marca).filter_by(disciplina = disciplina, user_id = id).join(User_register, User_register.id == Marca.user_id).order_by(Marca.date.asc()).all()            
            user = np.unique([row[2] + " " + row[3] for row in all_marks])
            minimo = (np.amin(np.array([row[1] for row in all_marks]))).strftime("%H:%M:%S.%f")
            maximo = (np.amax(np.array([row[1] for row in all_marks]))).strftime("%H:%M:%S.%f")
            maxmin = [minimo[0:-4], maximo[0:-4]]
            if maxmin[0] == maxmin[1]:
                maxmin[1] = maxmin[0][0:-7] + str(int(maxmin[0][-7:-6]) + 1) + maxmin[0][5:]
            date = [row[0].strftime("%d/%m/%Y") for row in all_marks]
            time = [row[1].strftime("%H:%M:%S.%f") for row in all_marks]
            return [date, time, 3, maxmin, user]
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

        --> Insert_user: insert new record for  User table
        --> update_password: Set new password record for  User table
        --> get_all_user: Get all records from User table
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

def get_all_user():
    '''
        Return all records from User table
    '''
    return db.session.query(User_register.id, User_register.name, User_register.surname).order_by(User_register.name).all()


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

def get_all_test_admin(ids):
    '''
        def 
            Select all register for ids on Test table
        INPUT
            ID --> INT
        OUTPUT 
            array --> succesfull\n
            false --> something wrong
    '''
    try:
        all_test = db.session.query(User_register.name, User_register.surname, test).select_from(test).join(User_register, User_register.id == test.user_id).filter(or_(*[test.user_id.like(id) for id in ids])).all()
        return all_test
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
        all_marks = db.session.query(test.date, test.mark, test.repeticiones, User_register.name, User_register.surname).select_from(test).filter_by(user_id = id, test_name = tipo_test).join(User_register, User_register.id == test.user_id).order_by(test.date.asc()).all()               
        date = [row[0].strftime("%d/%m/%Y") for row in all_marks]
        time = [(row[1] / (1.0278 - 0.0278 * row[2])) for row in all_marks]
        actual = calculate_rm(time[-1])
        user = np.unique([row[3] + " " +row[4] for row in all_marks])
        return [date, time, actual, user]
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


def prueba():
    pruebas = ['50m MASC. PC', '60m MASC. PC', '200m MASC. PC', '300m MASC. PC', '400m MASC. PC', '500m MASC. PC', '600m MASC. PC', '800m MASC. PC', 
'1.000m MASC. PC', '1.500m MASC. PC', '2.000m MASC.PC', '3.000m MASC. PC', '60m vallas (0,84) MASC. PC', '60m vallas (0,91) Sub16-Máster MASC. PC', 
'60m vallas (0,91) MASC. PC', 'Altura MASC. PC', 'Pértiga MASC. PC', 'Longitud MASC. PC', 'Triple Salto MASC. PC', 'Peso (2kg) MASC. PC', 'Peso (3kg) MASC. PC','Peso (4kg) MASC. PC', 'Peso (5kg) MASC. PC', 'Triatlón Sub12 MASC. PC', 
 '5km Ruta Masc.', '10km Ruta Masc.', 'Medio Maratón MASC.', '2km Marcha MASC. RUTA', '60m FEM. PC', '50m FEM. PC', '200m FEM. PC', '300m FEM. PC', '400m FEM. PC', '500m FEM. PC', '600m FEM. PC', '800m FEM. PC', '1.000m FEM. PC', '2.000m FEM. PC', '3.000m FEM. PC', '60m vallas (0,762) Sub14 FEM. PC', '60m vallas (0,762) FEM. PC', '60m vallas (0,84) FEM. PC', 'Altura FEM. PC', 'Longitud FEM. PC', 'Triple Salto FEM. PC', 'Peso (2kg) FEM. PC', 'Peso (3kg) FEM. PC', 'Peso (4kg) FEM. PC', 'Triatlón Sub10 FEM PC', 'Triatlón Sub12 FEM PC', '10km Ruta FEM.', 'Medio Maratón FEM.', 'Maratón FEM.', '1km Marcha FEM. RUTA', '2km Marcha FEM. RUTA', '3km Marcha FEM. RUTA', '50m MASC. AL', '200m MASC. AL', 'Longitud MASC. AL', '4x50m MASC. AL', '500m MASC. AL', '1.000m MASC. AL', 'Altura MASC. AL', 'Peso (2kg) MASC. AL', 
 '60m MASC. AL', '600m MASC. AL', 'Jabalina Vortex MASC.', '4x60m MASC. AL', 
 '80m MASC. AL', '150m MASC. AL', '80m vallas (0,84) MASC. AL', 
 '60m vallas (0,84) MASC. AL', 'Peso (3kg) MASC. AL', 'Disco (800g) MASC.', 'Jabalina (500g) MASC.', '4x80m MASC. AL', '100m MASC. AL',
  '300m MASC. AL', '3.000m MASC. AL', '300m vallas (0,84) MASC. AL', '1.500m Obst. MASC.', 'Triple Salto MASC. AL', 'Peso (4kg) MASC. AL', 'Disco (1kg) MASC.', 
  'Martillo (4kg) MASC.', 'Jabalina (600g) MASC.', '4x100m MASC. AL', '4x300m MASC. AL', '400m MASC. AL', '800m MASC. AL', '1.500m MASC. AL', 
  '110m vallas (1,00) MASC. AL', '110m vallas (0,914) MASC. AL', '400m vallas (0,91) MASC. AL', 'Peso (5kg) MASC. AL', 'Disco (1,5kg) MASC.', 
  'Martillo (5kg) MASC.', 'Martillo (6kg) MASC.', 'Jabalina (700g) MASC.', '3.000m Obst. MASC.', 'Pértiga MASC. AL', 'Peso (6kg) MASC. AL',
   'Peso (7,260kg) MASC. AL', 'Disco (1,750kg) MASC.', 'Jabalina (800g) MASC.', '4x400m MASC. AL', 'Disco (2kg) MASC.', 'Martillo (7,260kg) MASC.', 
   '3.000m Marcha MASC. en pista', '10.000m MASC. AL', 'Martillo Pesado (11,34kg) MASC.', '50m FEM. AL', '200m FEM. AL', 'Longitud FEM. AL', '4x50m FEM. AL',
    '500m FEM. AL', '1.000m FEM. AL', 'Altura FEM. AL', '1.000m Marcha FEM. en pista', '60m FEM. AL', '600m FEM. AL', 'Peso (2kg) FEM AL', 'Jabalina Vortex FEM.', 
    '2.000m Marcha FEM. en pista', '4x60m FEM. AL', '80m FEM. AL', '150m FEM AL', '60m vallas (0,762) Sub14 FEM. AL', '80m vallas (0,762) FEM. AL',
     'Triple Salto FEM. AL', 'Peso (3kg) FEM. AL', 'Jabalina (400g) FEM.', '4x80m FEM. AL', '100m FEM. AL', '300m FEM. AL', '3.000m FEM. AL',
      '100m vallas (0,762) Sub18/Sub16 FEM. AL', '300m vallas (0,762) FEM. AL', 'Disco (800g) FEM.', 'Martillo (3kg) FEM.', 'Jabalina (500g) FEM.',
       '3.000m Marcha FEM. en pista', '4x100m FEM. AL', '4x300m FEM. AL', '400m FEM. AL', '800m FEM. AL', '1.500m FEM. AL', '400m vallas (0,762) FEM. AL', 
       'Disco (1kg) FEM.', 'Martillo (4kg) FEM.', 'Jabalina (600g) FEM.', '3.000m Obst. FEM.', '4x400m FEM. AL', '100m vallas (0,84) FEM. AL', 'Peso (4kg) FEM. AL']


    lanzamientos = []

    saltos = []

    velocidad = []

    vallas = []

    marcha = [] 

    fondoMedioFondo = []

    medioYvelocidad = []
    f = ('todos.html', 'w')
    count = 0
    for x in pruebas:
        for p in x.split(' '):
            if p in ['Disco', 'Jabalina', 'Martillo', 'Peso']:
                lanzamientos.append(x)
                break
            elif p in ['vallas']:
                vallas.append(x)
                break
            elif p in ['Triple', 'Longitud', 'Pértiga', 'Altura']:
                saltos.append(x)
                break
            elif p in ['Marcha']:
                marcha.append(x)
                break
            if p == x.split(' ')[-1]:
                medioYvelocidad.append(x)

    for x in medioYvelocidad:
        for p in x.split(' '):
            if p in ['50m', '60m', '80m', '100m', '150m', '200m','300m', '400m']:
                velocidad.append(x)
                break
            if p == x.split(' ')[-1]:
                fondoMedioFondo.append(x)     

    lanzamientos.sort()
    saltos.sort()
    velocidad.sort()
    vallas.sort()
    marcha.sort()
    fondoMedioFondo.sort()

    todos = [lanzamientos, saltos, velocidad, vallas, marcha, fondoMedioFondo]
    

    copia = [['600m MASC. PC', '1:33.70', 'TARDIO TORRENTE, MIGUEL ANGEL', '12/03/2022'], ['1.000m MASC. PC', '2:51.31', 'TARDIO TORRENTE, MIGUEL ANGEL', '05/03/2022'], ['600m MASC. AL', '1:34.15', 'TARDIO TORRENTE, MIGUEL ANGEL', '06/03/2022'], ['1.000m MASC. AL', '2:54.85', 'TARDIO TORRENTE, MIGUEL ANGEL', '15/01/2022'], ['3.000m MASC. AL', '11:06.40', 'TARDIO TORRENTE, MIGUEL ANGEL', '08/05/2022'], ['1.500m Obst. MASC.', '5:37.17', 'TARDIO TORRENTE, MIGUEL ANGEL', '23/04/2022'], ['Disco (1kg) MASC.', '30.24', 'TARDIO TORRENTE, MIGUEL ANGEL', '10/04/2022'], ['Jabalina (600g) MASC.', '27.73', 'TARDIO TORRENTE, MIGUEL ANGEL', '27/02/2022'], ['600m MASC. AL', '1:34.15', 'TARDIO TORRENTE, MIGUEL ANGEL', '06/03/2022'], ['1.500m Obst. MASC.', '5:37.17', 'TARDIO TORRENTE, MIGUEL ANGEL', '23/04/2022'], ['Disco (1kg) MASC.', '30.24', 'TARDIO TORRENTE, MIGUEL ANGEL', '10/04/2022'], ['Jabalina (600g) MASC.', '27.73', 'TARDIO TORRENTE, MIGUEL ANGEL', '27/02/2022']] 
    all_user = db.session.query(User_register.id, User_register.name, User_register.surname).filter_by(id = 44).order_by(User_register.name).all()
    for x in all_user:
        print((x[2] + ', ' + x[1]).upper())
        for r in copia:
            if r[2] == (x[2] + ', ' +x[1]).upper():
                fecha = r[3][6:] + '-' + r[3][3:5] + '-' + r[3][0:2]
                if r[0] in lanzamientos:
                    insert_mark('Lanzamientos', fecha, r[1], r[0], x[0])
                elif r[0] in saltos:
                    insert_mark('Saltos', fecha, r[1], r[0], x[0])
                elif r[0] in velocidad:
                    marca = '00:' + r[1]
                    insert_mark('Velocidad', fecha,  marca, r[0], x[0])
                elif r[0] in vallas:
                    marca = '00:' + r[1]
                    insert_mark('Vallas', fecha, marca,  r[0], x[0])
                elif r[0] in marcha:
                    insert_mark('Marcha', fecha, r[1], r[0], x[0])
                elif r[0] in fondoMedioFondo:
                    insert_mark('Fondo / Medio Fondo', fecha, r[1], r[0], x[0])


                        