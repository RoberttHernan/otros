from flask import Flask

# crea la aplicacion mediante Flask
app = Flask(__name__)



#configuracion de la base de datos

DB_CONFIG = {
    


}



#definir la primera ruta de la aplicacion (la raiz o pagina de inicio)
@app.route('/')
def inicio ():
    return '<h1>Hola, este es mi primer servidor web</h1>'

#definir una segunda ruta para mostrar un mensaje diferente
@app.route ('/sobre-mi')
def sobre_mi():
    return '<h1>Hola, soy un desarrollador web en aprendizaje</h1>'



#ejecutar la aplicacion

if __name__ == '__main__':
    app.run(debug=True)