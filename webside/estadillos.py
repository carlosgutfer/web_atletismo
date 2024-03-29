from . import calculos_puntos as cp
import numpy as np
import copy

def sorter(item):
    return (item[0])

def borrar_huecos(final_marks):
    deleteKeys = [delete for delete in final_marks if final_marks[delete] == []]
    for i in deleteKeys:
        del final_marks[i]
    return final_marks

def borrar_marca(estadillo_posible):
    borrar_marca = {}
    for key,value in estadillo_posible.items():
        for key_2, value_2 in estadillo_posible.items():
            if key != key_2:
                nombre = value[2] + value[3] 
                if value[2] + value[3] == value_2[2] + value_2[3] and value < value_2:
                    borrar_marca[key] = value
    borrar_peor = []
    for key, values in borrar_marca.items():
         for key_2, values_2 in borrar_marca.items():
            if values[0] > values_2[0] and values_2[2] + values_2[3] == values[2] + values[3]:
                if key_2 not in borrar_peor:
                    borrar_peor.append(key_2)
    for datos in borrar_peor:
        del borrar_marca[datos]
    if len(borrar_peor) > 0:
        borrar_marca = borrar_huecos(borrar_marca)

    return borrar_marca

def comprobar_fin(resultado, check_name,final_marks):
    estadillo = []
    fin = False
    for key,values in resultado[4].items():
        estadillo.append(values)
    for key,values in check_name.items():
        estadillo.append(values[0])
    nombres_apellidos = [marca[2] + marca[3] for marca in estadillo]
    if len(nombres_apellidos) != len(set(nombres_apellidos)):
        return estadillo, fin 
    prueba_participante = [marca[1].disciplina  for marca in estadillo]
    for key,value in final_marks.items():
        modificacion = False
        for marcas in value:
            nombre =  marcas[2] + marcas[3]
            if nombre  in nombres_apellidos:
                fin = True
                if prueba_participante[nombres_apellidos.index(nombre)] == key or prueba_participante[nombres_apellidos.index(nombre)] in '60m MASC. PC/100m MASC. AL':
                    break    
                if modificacion:
                    fin = False
            else:
                modificacion = True
    return estadillo, fin 

def mejor_marca_atleta(final_marks):
    #Deja solo la mejor marca de cada atleta en cada prueba
    for key,values in final_marks.items():
        valores_eliminar = []
        for i in range(len(values)):
            for j in range(i + 1,len(values)):
                if values[i][2] + values[i][3] == values[j][2] + values[j][3] and values[i][0] >= values[j][0] :
                    if values[i] not in valores_eliminar:
                        valores_eliminar.append(values[i])
        for valores in valores_eliminar:
            values.remove(valores)
    return final_marks

def buscar_estadillo_aux(copia_marks_sin_unos,mejor_estadillo, j, contador, longitud_inferior):
    #Compruebo si los nombres y puntos de cada usuario en cada prueba son lo mejor sin repetir 
    if len(copia_marks_sin_unos) == 1:
        estadillo_posible = {}
        marca = copia_marks_sin_unos[list(copia_marks_sin_unos.keys())[0]]
        estadillo_posible[list(copia_marks_sin_unos.keys())[0]] = marca[0]
        contador = 10000000
        return [copia_marks_sin_unos,[[0,len(marca)]], j, contador,estadillo_posible]
    while True:
        if mejor_estadillo[j][0] + 1 < mejor_estadillo[j][-1]:
            estadillo_posible = {}
            i = -1
            for item,value in copia_marks_sin_unos.items():
                i += 1
                estadillo_posible[item] = value[mejor_estadillo[i][0]]
            todos_nombres_apellidos = [value[2] + ' ' +value[3] for key,value in estadillo_posible.items()] 
            mejor_estadillo[j][0] += 1
            if len(set(todos_nombres_apellidos)) == len(todos_nombres_apellidos):
                return [copia_marks_sin_unos,mejor_estadillo, j, contador,estadillo_posible]
            if len(set(todos_nombres_apellidos)) == longitud_inferior:
                return borrar_marca(estadillo_posible)
                
        else:
            mejor_estadillo[j][0] = 0
            if j + 1 <  len(mejor_estadillo):
                j +=1
            else:
                j = 0
            for numeros in mejor_estadillo:
                if mejor_estadillo[j][0] + 1 < mejor_estadillo[j][-1]:
                    mejor_estadillo[j][0] += 1
                    j = 0
                    break
                else:
                    mejor_estadillo[j][0] = 0
                    if j + 1 <  len(mejor_estadillo):
                        j +=1
                    else:
                        j = 0

        contador += 1
        if contador == 50000:
            break
    return [copia_marks_sin_unos,mejor_estadillo, j, contador,estadillo_posible]

def calculo_pruebas_con_varios_participantes(final_marks):

    check_name = {}
    copia_marks_sin_unos = {}

    #Guarda las pruebas que solo tienen 1 participante y creo el diccionario copia 
    for key,values in final_marks.items():
        if len(values) == 1:
            check_name[key] = values
        else:
            copia_marks_sin_unos[key] = values
    
    if len(copia_marks_sin_unos) == 0:
        mejor_estadillo = []
        for key,values in check_name.items():
            mejor_estadillo.append([0,len(values)])
        estadillo_calculado = {}
        for item,values in check_name.items():
            estadillo_calculado[key] = values[0] 
        estadillo_posible = [check_name,mejor_estadillo,0,0,estadillo_calculado]
        return [],check_name, estadillo_posible


    longitud_inferior = 0
    todos_nombres_apellidos = []
    for key,value in copia_marks_sin_unos.items():
        for nombres in value:
            todos_nombres_apellidos.append(nombres[2] + ' ' +nombres[3])
    if len(set(todos_nombres_apellidos)) < len(copia_marks_sin_unos):
       longitud_inferior =  len(set(todos_nombres_apellidos))
        
    #Creo un array de las posiciones de cada prueba
    mejor_estadillo = []
    for key,values in copia_marks_sin_unos.items():
        mejor_estadillo.append([0,len(values)])

    #Calculo un primer estadillo sin repeticion
    estadillo_posible = [copia_marks_sin_unos,mejor_estadillo,0,0]
    resultado = []
    contador = 0
    estadillo_posible = buscar_estadillo_aux(estadillo_posible[0],estadillo_posible[1],estadillo_posible[2],estadillo_posible[3], longitud_inferior)
    if isinstance(estadillo_posible,dict):
        return estadillo_posible
    contador +=1
    resultado = estadillo_posible[4]

    #Compruebo si tengo que borrar algun atleta del estadillo posible porque me interesa mejor su marca individual
    borrar_de_check_name = []
    nombres_check_name = [value[0][2] + value[0][3] for key, value in check_name.items()]
    for key_resultado,atletas in resultado.items():
        for key,value in check_name.items():
            if atletas[2] + atletas[3] == value[0][2] + value[0][3]:
                for values_marks in final_marks[key_resultado]:
                    if values_marks[2] +values_marks[3] != atletas[2] + atletas[3]:
                        if values_marks[0] < atletas[0] and values_marks[0] + value[0][0] > atletas[0]:
                            if values_marks[2] +values_marks[3] not in  nombres_check_name:
                                if [key_resultado,atletas] not in borrar_de_check_name:
                                    borrar_de_check_name.append([key_resultado,atletas])
    return borrar_de_check_name,check_name, estadillo_posible

def comprobar_si_mejor_marca_usuario(final_marks,borrar_de_check_name):

    mayor = []
    for prueba,marcas in borrar_de_check_name.items():
        nuevo = []
        romper = False
        for key,values in final_marks.items():
            if romper:
                break
            if key != prueba:
                for i in range(len(values)):
                    if marcas[0][2] + marcas[0][3] == values[i][2] + values[i][3]: 
                        if marcas[0][0] >  values[i][0]:
                            nuevo.append([key,values[i]])
                        elif marcas[0][0] <  values[i][0]: 
                            romper = True
                            break
        if not romper and mayor != []:
            mayor.append(nuevo)      
    if  len(mayor) > 0:
        for personas in mayor:
            for marcas in personas:
                final_marks[marcas[0]].remove(marcas[1])
    return final_marks

def borrar_duplicados_unico_usuario(check_name,final_marks):
    #Si hay un usuario que es único en varias pruebas. Voy a dejar solo en la prueba donde tenga más puntos
    borrar_peor = []
    for key, values in check_name.items():
         for key_2, values_2 in check_name.items():
            if values[0][0] < values_2[0][0] and values_2[0][2] + values_2[0][3] == values[0][2] + values[0][3]:
                if [key,values] not in borrar_peor:
                    borrar_peor.append([key,values])
    for datos in borrar_peor:
        final_marks[datos[0]].remove(datos[1][0])
    if len(borrar_peor) > 0:
        final_marks = borrar_huecos(final_marks)
        check_name = borrar_huecos(check_name)
    return final_marks,check_name

def mejor_marca_unico_usuario_por_prueba(final_marks):
    #Si hay un usuario que es único en varias pruebas. Voy a dejar solo en la prueba donde tenga más puntos
    borrar_peor = []
    for key, values in final_marks.items():
         for key_2, values_2 in final_marks.items():
            if values[0][0] < values_2[0][0] and values_2[0][2] + values_2[0][3] == values[0][2] + values[0][3]:
                if [key,values] not in borrar_peor:
                    borrar_peor.append([key,values])
    for datos in borrar_peor:
        final_marks[datos[0]].remove(datos[1][0])
    if len(borrar_peor) > 0:
        final_marks = borrar_huecos(final_marks)
    return final_marks

def comprobar_mejor_combinacion(final_marks,check_name):
    # Compruebo en las pruebas que tienen más de un usuario el usuario seleccionado es su mejor marca combianda,
    #para ello comprueba si  tomando otra prueba donde esté el individual y sumandoselo a una peor donde el está 
    #combinado la súma es superior a la marca de combinado
    del_key =[]
    for key_check,values_check in check_name.items():
        mejor = False
        for key_final,value_final in final_marks.items():
            if mejor:
                break
            if key_check != key_final:
                puntuacion_maxima = 0
                for mark in value_final:
                    if mejor:
                        break
                    if values_check[0][2] + values_check[0][3]   == mark[2] + mark[3]:
                        puntuacion_maxima = mark[0]
                        for mark in value_final:
                            if values_check[0][2] + values_check[0][3]   != mark[2] + mark[3] and mark not in value_final[0]:
                                puntuacion_parcial = values_check[0][0] + mark[0]
                                if puntuacion_maxima < puntuacion_parcial:
                                    del_key.append([values_check[0][2] + values_check[0][3],key_final]) 
                                    mejor = True                              
                                    break
        
    for key,values in final_marks.items():
        if len(values) > 1:
            valor_borrar = []
            for i in range(len(values)):
                nombre_apellido = values[i][2] + values[i][3]
                for nombres in del_key:
                    if nombre_apellido == nombres[0] and key == nombres[1]:
                        valor_borrar.append(values[i])
            if valor_borrar != []:
                for valor in valor_borrar:
                    if valor in values:
                        values.remove(valor)
    return final_marks

def modificar_valor(resultado,final_marks,):

    # co,pruebo que el usuario no tiene más marcas por encima 
    nombres_apellidos = [value[2] + value[3] for key,value in resultado[4].items()]
    mod = {}
    borrar_final = {}
    for key_resultado,value_resultado in resultado[4].items():
        for key_final, value_final in final_marks.items():
            if key_resultado == key_final:
                for data in value_final:
                    if data[0] > value_resultado[0] and data[2] + data[3] not in nombres_apellidos:
                        if key_resultado not in mod.keys() and key_resultado not in borrar_final.keys():
                            mod[key_resultado] = data
                            borrar_final[key_resultado] = value_resultado
                        elif  mod[key_resultado][0] <  data[0]:    
                            mod[key_resultado] = data
                            borrar_final[key_resultado] = value_resultado
    
    #Veo que no se repita el nombre en ninguna de las nuevas marcas a introducir en resultado.
    #si se repite tomo solo la mejor.
    borrar_mod = {}
    for key,value in mod.items():
        for key_2,value_2 in mod.items():
            if key != key_2 and value[2] + value[3] == value_2[2] + value_2[3]:
                if value[0] > value_2[0]:
                        borrar_mod[key_2] = value_2
                else:
                        borrar_mod[key] = value

    for key,value in borrar_mod.items():
        del mod[key]

    for key,value in mod.items():
        resultado[4][key] = value  
    for key,value in borrar_final.items():
        if value in  final_marks[key]:
            final_marks[key].remove(value)
    return mod,resultado,final_marks

def calculo_estadillo(final_marks):
   
    copia_final_marks = {}
    copia_check_name = {}
    maximo = 0
    fin = False
    contador = 0
    while True:
        contador += 1
        borrar_de_check_name = True
        if sum(len(value) for key, value in final_marks.items()) == len(final_marks):
            final_marks = mejor_marca_unico_usuario_por_prueba(final_marks)
            estadillo = [values[0] for key,values in final_marks.items()]
            maximo = np.sum(np.array([marca[0] for marca in estadillo]))
            return [estadillo,maximo]
        while borrar_de_check_name != []:
            calculo = calculo_pruebas_con_varios_participantes(final_marks)
            if isinstance(calculo,dict):
                for key,value in calculo.items():
                    final_marks[key].remove(value)
                continue
            borrar_de_check_name,check_name, resultado = calculo
            if borrar_de_check_name != []:
                for datos in borrar_de_check_name:
                    final_marks[datos[0]].remove(datos[1])
        final_marks = comprobar_si_mejor_marca_usuario(final_marks, check_name)
        check_name = borrar_huecos(check_name)
        final_marks = comprobar_mejor_combinacion(final_marks,check_name)
        final_marks = borrar_huecos(final_marks)
        final_marks, check_name = borrar_duplicados_unico_usuario(check_name,final_marks)
        mod, resultado,final_marks = modificar_valor(resultado,final_marks)
        estadillo, fin = comprobar_fin(resultado, check_name,final_marks)
        if fin:
            break



        if copia_final_marks == final_marks and check_name == copia_check_name:
            mod = True
            while(mod != {}):
                mod, resultado,final_marks = modificar_valor(resultado,final_marks)
                estadillo, fin = comprobar_fin(resultado, check_name,final_marks)
                if fin:
                    mod = {}
            if fin:  
                break 
        else:
            copia_final_marks = final_marks
            copia_check_name = check_name
    
    
    
        if contador == 10000:
            break
    maximo = np.sum(np.array([marca[0] for marca in estadillo]))
    return [estadillo,maximo]

def estadillo_sub16_masculino_al(groups):
    '''
    def 
    return list with the best marks 
    INPUT
        - List of marks 
    OUTPUT
        - SUCCESFULL: LIST OF BEST MARKS \n
        - WRONG: False
    '''
    final_marks =  {
                    '60m MASC. PC': [],
                    '100m MASC. AL': [],
                    '300m MASC. AL': [],
                    '60m vallas (0,91) Sub16-Master MASC. PC': [],
                    '60m vallas (0,91) MASC. PC': [],
                    '100m vallas (0,914) MASC. AL': [],
                    '300m vallas (0,84) MASC. AL': [],
                    '600m MASC. AL': [],
                    '1.000m MASC. AL': [],
                    '3.000m MASC. AL': [],
                    'Disco (1kg) MASC.': [],
                    'Martillo (4kg) MASC.': [],
                    'Peso (4kg) MASC. AL': [],
                    'Jabalina (600g) MASC.': [],
                    'Longitud MASC. AL': [],
                    'Triple Salto MASC. AL': [],
                    'Altura MASC. AL': [],
                    'Pertiga MASC. AL': []
                }

    for group in groups:
        if group in final_marks.keys():
            aux = groups.get(group)
            for x in aux:
                if x.Marca.sector == 'Lanzamientos' and 'FEM' not in x.Marca.disciplina:
                    puntos = int(cp.calcular_puntos_lanzamientos_masc(x.Marca))
                    union = list(x)
                    union.insert(0,puntos)
                    final_marks[group].append(union)
                elif x.Marca.sector == 'Saltos' and 'FEM' not in x.Marca.disciplina:
                    puntos = int(cp.calcular_puntos_saltos_masc(x.Marca))
                    union = list(x)
                    union.insert(0,puntos)
                    final_marks[group].append(union)
                elif x.Marca.sector == 'Vallas' and 'FEM' not in x.Marca.disciplina:
                    puntos = int(cp.calcular_puntos_vallas_masc(x.Marca))
                    union = list(x)
                    union.insert(0,puntos)
                    final_marks[group].append(union)
                elif x.Marca.sector == 'Velocidad' and 'FEM' not in x.Marca.disciplina:
                    puntos = int(cp.calcular_puntos_velocidad_masc(x.Marca))
                    union = list(x)
                    union.insert(0,puntos)
                    final_marks[group].append(union)
                elif x.Marca.sector == 'Fondo / Medio Fondo' and 'FEM' not in x.Marca.disciplina:
                    puntos = int(cp.calcular_puntos_fondo_masc(x.Marca))
                    union = list(x)
                    union.insert(0,puntos)
                    final_marks[group].append(union)
    estadillo = []

    #Unificar vallas y velocidad
    final_marks['60m MASC. PC' +'/100m MASC. AL'] = []
    final_marks['60m vallas (0,91) MASC. PC' + '/100m vallas (0,914) MASC. AL'] = []
    for key,values in final_marks.items():
        if  key in ['60m MASC. PC','100m MASC. AL']:
            for marks in values:
                final_marks['60m MASC. PC' +'/100m MASC. AL'].append(marks)
        elif  key in ['60m vallas (0,91) Sub16-Master MASC. PC','60m vallas (0,91) MASC. PC','100m vallas (0,914) MASC. AL']:
            for marks in values:
                final_marks['60m vallas (0,91) MASC' + '/100m vallas (0,914) MASC'].append(marks)
                
    #Borro vallas y velocidad suelta. Y ordeno ambos
    borrar_valas_velocidad = ['60m MASC. PC','100m MASC. AL','60m vallas (0,91) MASC. PC','60m vallas (0,91) Sub16-Master MASC. PC','100m vallas (0,914) MASC. AL']
    for i in borrar_valas_velocidad:
        del final_marks[i]
    final_marks['60m MASC. PC/100m MASC. AL'] = sorted(final_marks['60m MASC. PC/100m MASC. AL'], key = sorter)
    final_marks['60m vallas (0,91) MASC. PC/100m vallas (0,914) MASC. AL'] = sorted(final_marks['60m vallas (0,91) MASC. PC/100m vallas (0,914) MASC. AL'], key =  sorter)

    #Borrar huecos libres
    final_marks = borrar_huecos(final_marks)
    
    #Ordeno todas las listas de mayor a menor 
    for key,values in final_marks.items():
        if values[0][1].sector not in ['Lanzamientos', 'Saltos']:
            final_marks[key] = sorted(values, key = sorter)[::-1]

    final_marks = mejor_marca_atleta(final_marks)
    for key,values in final_marks.items():
        values = sorted(values, key = sorter)
        estadillo.append(values[-1])
    copia = copy.deepcopy(final_marks)
    estadillo,maximo = calculo_estadillo(final_marks)
    
    return estadillo, maximo, copia
  
def estadillo_sub16_femenino_al(groups):
    '''
    def 
    return list with the best marks 
    INPUT
        - List of marks 
    OUTPUT
        - SUCCESFULL: LIST OF BEST MARKS \n
        - WRONG: False
    '''
    final_marks =  {
                    '60m FEM. PC': [],
                    '100m FEM. AL': [],
                    '300m FEM. AL': [],
                    '60m vallas (0,0762) FEM. PC': [],
                    '100m vallas (0,762) Sub18/Sub16 FEM. AL': [],
                    '300m vallas (0,762) FEM. AL': [],
                    '600m FEM. AL': [],
                    '1.000m FEM. AL': [],
                    '3.000m FEM. AL': [],
                    'Disco (800g) FEM.': [],
                    'Martillo (3kg) FEM.': [],
                    'Peso (3kg) FEM. PC': [],
                    'Jabalina (500g) FEM.': [],
                    'Longitud FEM. AL': [],
                    'Triple Salto FEM. AL': [],
                    'Altura FEM. AL': [],
                    'Pertiga FEM. AL': []
                }

    for group in groups:
        if group in final_marks.keys():
            aux = groups.get(group)
            for x in aux:
                if x.Marca.sector == 'Lanzamientos':
                    puntos = int(cp.calcular_puntos_lanzamientos_fem(x.Marca))
                    union = list(x)
                    union.insert(0,puntos)
                    final_marks[group].append(union)
                elif x.Marca.sector == 'Saltos':
                    puntos = int(cp.calcular_puntos_saltos_fem(x.Marca))
                    union = list(x)
                    union.insert(0,puntos)
                    final_marks[group].append(union)
                elif x.Marca.sector == 'Vallas':
                    puntos = int(cp.calcular_puntos_vallas_fem(x.Marca))
                    union = list(x)
                    union.insert(0,puntos)
                    final_marks[group].append(union)
                elif x.Marca.sector == 'Velocidad':
                    puntos = int(cp.calcular_puntos_velocidad_fem(x.Marca))
                    union = list(x)
                    union.insert(0,puntos)
                    final_marks[group].append(union)
                elif x.Marca.sector == 'Fondo / Medio Fondo':
                    puntos = int(cp.calcular_puntos_fondo_fem(x.Marca))
                    union = list(x)
                    union.insert(0,puntos)
                    final_marks[group].append(union)
    estadillo = []

    #Unificar vallas y velocidad
    final_marks['60m FEM. PC' +'/100m FEM. AL'] = []
    final_marks['60m vallas (0,0762) FEM. PC' + '/100m vallas (0,762) Sub18/Sub16 FEM. AL'] = []
    for key,values in final_marks.items():
        if  key in ['60m FEM. PC','100m FEM. AL']:
            for marks in values:
                final_marks['60m FEM. PC' +'/100m FEM. AL'].append(marks)
        elif  key in ['60m vallas (0,0762) FEM. PC','100m vallas (0,762) Sub18/Sub16 FEM. AL']:
            for marks in values:
                final_marks['60m vallas (0,0762) FEM. PC' + '/100m vallas (0,762) Sub18/Sub16 FEM. AL'].append(marks)
                
    #Borro vallas y velocidad suelta. Y ordeno ambos
    borrar_valas_velocidad = ['60m FEM. PC','100m FEM. AL','60m vallas (0,0762) FEM. PC','100m vallas (0,762) Sub18/Sub16 FEM. AL']
    for i in borrar_valas_velocidad:
        del final_marks[i]
    final_marks['60m FEM. PC/100m FEM. AL'] = sorted(final_marks['60m FEM. PC/100m FEM. AL'], key = sorter)
    final_marks['60m vallas (0,0762) FEM. PC/100m vallas (0,762) Sub18/Sub16 FEM. AL'] = sorted(final_marks['60m vallas (0,0762) FEM. PC/100m vallas (0,762) Sub18/Sub16 FEM. AL'], key =  sorter)

    #Borrar huecos libres
    final_marks = borrar_huecos(final_marks)
    
    #Ordeno todas las listas de mayor a menor 
    for key,values in final_marks.items():
        if values[0][1].sector not in ['Lanzamientos', 'Saltos']:
            final_marks[key] = sorted(values, key = sorter)[::-1]

    final_marks = mejor_marca_atleta(final_marks)
    for key,values in final_marks.items():
        values = sorted(values, key = sorter)
        estadillo.append(values[-1])
    copia = copy.deepcopy(final_marks)
    estadillo,maximo = calculo_estadillo(final_marks)

    return estadillo, maximo, copia



