from webside import create_app
from flask import send_from_directory

app = create_app()


@app.route('/mostrar_imagen/<nombre_archivo>')
def mostrar_imagen(nombre_archivo):
    return send_from_directory('images', nombre_archivo)

if __name__ == '__main__':
    app.run(debug= True)

