import datetime

def calcular_puntos_lanzamientos_masc(marca):
    if 'Peso' in marca.disciplina:
        return 0.042172*(marca.meters + 687.7)**2 - 20000
    elif 'Disco' in marca.disciplina:
        return 0.004007*(marca.meters + 2232.6)**2 - 20000
    elif 'Martillo' in marca.disciplina:
        return 0.0028038*(marca.meters + 2669.4)**2-20000
    elif 'Jabalina' in marca.disciplina:
        return 0.0023974 * (marca.meters + 2886.8)** 2 - 20000

def calcular_puntos_lanzamientos_fem(marca):
    if 'Peso' in marca.disciplina:
        return 0.0462*(marca.meters + 657.53)**2 - 20000
    elif 'Disco' in marca.disciplina:
        return 0.0040277*(marca.meters + 2227.3)**2 - 20000
    elif 'Martillo' in marca.disciplina:
        return 0.0030965*(marca.meters + 2540)**2-20000
    elif 'Jabalina' in marca.disciplina:
        return 0.004073 * (marca.meters + 2214.9)** 2 - 20000

def calcular_puntos_saltos_masc(marca):
    if 'Triple' in marca.disciplina:
        return 0.4611*(marca.meters + 98.63) ** 2 - 5000
    elif 'Longitud' in marca.disciplina:
        return 1.929 * (marca.meters + 48.41) ** 2 - 5000
    elif 'Pertiga' in marca.disciplina:
        return 3.042 * (marca.meters + 39.39) ** 2 - 5000
    elif 'Altura' in marca.disciplina:
        return 32.29 * (marca.meters + 11.534) ** 2 - 5000

def calcular_puntos_saltos_fem(marca):
    if 'Triple' in marca.disciplina:
        return 0.4282*(marca.meters + 105.53) ** 2 - 5000
    elif 'Longitud' in marca.disciplina:
        return 1.966 * (marca.meters + 49.24) ** 2 - 5000
    elif 'Pertiga' in marca.disciplina:
        return 3.953 * (marca.meters + 34.83) ** 2 - 5000
    elif 'Altura' in marca.disciplina:
        return 39.34 * (marca.meters + 10.574) ** 2 - 5000

def calcular_puntos_velocidad_masc(marca):
    seconds = float(datetime.timedelta(hours=marca.time.hour, minutes=marca.time.minute, seconds=marca.time.second, milliseconds=marca.time.microsecond/1000).total_seconds())
    if '100m' in marca.disciplina:
        return 24.63 * (17 - seconds) ** 2
    elif '300m' in marca.disciplina:
        return 1.83 * (57.2 - seconds) ** 2
    elif '60m' in marca.disciplina:
        return 68.6 * (10.7 - seconds) ** 2

def calcular_puntos_velocidad_fem(marca):
    seconds = float(datetime.timedelta(hours=marca.time.hour, minutes=marca.time.minute, seconds=marca.time.second, milliseconds=marca.time.microsecond/1000).total_seconds())
    if '100m' in marca.disciplina:
        return 9.92 * (22 - seconds) ** 2
    elif '300m' in marca.disciplina:
        return 0.7 * (77 - seconds) ** 2
    elif '60m' in marca.disciplina:
        return 24.9 * (14 - seconds) ** 2

def calcular_puntos_vallas_masc(marca):
    seconds = float(datetime.timedelta(hours=marca.time.hour, minutes=marca.time.minute, seconds=marca.time.second, milliseconds=marca.time.microsecond/1000).total_seconds())
    if '110m' in marca.disciplina:
        return 7.66 * (25.8 - seconds) ** 2
    elif '100m' in marca.disciplina:
        return 7.66 * (25.8 - seconds) ** 2
    elif '60m' in marca.disciplina:
        return 23.9 * (14.6 - seconds) ** 2
    elif '300m' in marca.disciplina:
        return 0.546 * (95.5 - (seconds + 20)) ** 2

def calcular_puntos_vallas_fem(marca):
    seconds = float(datetime.timedelta(hours=marca.time.hour, minutes=marca.time.minute, seconds=marca.time.second, milliseconds=marca.time.microsecond/1000).total_seconds())
    if '100m' in marca.disciplina:
        return 3.98 * (30 - seconds) ** 2
    elif '60m' in marca.disciplina:
        return 11.16 * (18.2 - seconds) ** 2
    elif '300m' in marca.disciplina:
        return 0.208567 * (130 - (seconds + 20)) ** 2

def calcular_puntos_fondo_masc(marca):
    seconds = float(datetime.timedelta(hours=marca.time.hour, minutes=marca.time.minute, seconds=marca.time.second, milliseconds=marca.time.microsecond/1000).total_seconds())
    if '600m' in marca.disciplina:
        return 0.367 * (131 - seconds) ** 2
    elif '1.000m' in marca.disciplina:
        return 0.1074 * (240 - seconds) ** 2
    elif '3.000m' in marca.disciplina:
        return 0.00815 * (840 - seconds) ** 2 

def calcular_puntos_fondo_fem(marca):
    seconds = float(datetime.timedelta(hours=marca.time.hour, minutes=marca.time.minute, seconds=marca.time.second, milliseconds=marca.time.microsecond/1000).total_seconds())
    if '600m' in marca.disciplina:
        return 0.1192 * (184 - seconds) ** 2
    elif '1.000m' in marca.disciplina:
        return 0.0382 * (330 - seconds) ** 2
    elif '3.000m' in marca.disciplina:
        return 0.002539 * (1200 - seconds) ** 2 