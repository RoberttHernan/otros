# ============================================================
#  app.py — Aplicación principal Flask con MySQL
#
#  Implementa las 4 operaciones CRUD sobre la tabla `tareas`:
#    C reate  → /agregar
#    R ead    → /
#    U pdate  → /editar/<id>
#    D elete  → /eliminar/<id>
# ============================================================

# Flask      : micro-framework web (servidor, rutas, plantillas)
# request    : accede a los datos enviados por el navegador (formularios)
# redirect   : devuelve una respuesta HTTP 302 que redirige al cliente
# url_for    : genera URLs a partir del nombre de la función, evitando
#              escribir rutas a mano (más seguro ante cambios futuros)
from flask import Flask, render_template, request, redirect, url_for

# Driver oficial de MySQL para Python.
# Permite abrir conexiones, ejecutar SQL y obtener resultados.
import mysql.connector

# Crea la instancia de la aplicación Flask.
# __name__ indica a Flask dónde está el paquete raíz para localizar
# las carpetas 'templates/' y 'static/'.
app = Flask(__name__)

# ── Configuración de la base de datos ─────────────────────────
# Diccionario con los parámetros de conexión.
# Se pasa con ** (unpacking) a mysql.connector.connect().
DB_CONFIG = {
    'host': 'localhost',       # servidor MySQL (en este caso la misma máquina)
    'user': 'root',            # cambia por tu usuario de MySQL
    'password': 'tu_password', # cambia por tu contraseña de MySQL
    'database': 'taller_flask' # nombre de la base de datos creada en db.sql
}


def get_db():
    """
    Abre y devuelve una conexión nueva a MySQL.

    Se llama al inicio de cada ruta para obtener una conexión limpia.
    Es importante cerrarla con db.close() al terminar para liberar
    los recursos del servidor de base de datos.
    """
    return mysql.connector.connect(**DB_CONFIG)


# ── CREATE — Agregar tarea ─────────────────────────────────────
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    """
    GET  → muestra el formulario vacío (agregar.html)
    POST → lee los datos del formulario, los inserta en MySQL
           y redirige al listado principal.
    """
    if request.method == 'POST':
        # request.form es un diccionario con los campos del formulario HTML.
        # Los nombres ('titulo', 'descripcion') deben coincidir con el
        # atributo name="..." de cada <input> o <textarea>.
        titulo = request.form['titulo']

        # .get() devuelve '' si el campo no vino en el formulario (campo opcional).
        descripcion = request.form.get('descripcion', '')

        db = get_db()
        cursor = db.cursor()

        # %s es el marcador de posición (placeholder) de mysql-connector.
        # Nunca se debe construir SQL concatenando strings con f-strings o +,
        # porque eso abre la puerta a SQL Injection.
        # mysql-connector escapa automáticamente los valores antes de enviarlos.
        cursor.execute(
            'INSERT INTO tareas (titulo, descripcion) VALUES (%s, %s)',
            (titulo, descripcion)   # tupla con los valores reales
        )

        # commit() confirma la transacción en disco.
        # Sin commit() el INSERT no se guarda permanentemente.
        db.commit()
        db.close()

        # Redirige al usuario a la página principal (lista de tareas).
        # url_for('inicio') genera '/'.
        return redirect(url_for('inicio'))

    # Si la petición fue GET (el usuario solo abrió la página),
    # devuelve el formulario vacío.
    return render_template('agregar.html')


# ── READ — Listar todas las tareas ────────────────────────────
@app.route('/')
def inicio():
    """
    Consulta todas las tareas ordenadas de más reciente a más antigua
    y las pasa a la plantilla index.html para mostrarlas en tabla.
    """
    db = get_db()

    # dictionary=True hace que cada fila sea un dict {'id': 1, 'titulo': '...'}
    # en lugar de una tupla (1, '...').
    # Los dicts son más cómodos en las plantillas Jinja2: {{ tarea.titulo }}
    cursor = db.cursor(dictionary=True)

    # ORDER BY creada_en DESC → primero las tareas más nuevas (descendente).
    cursor.execute('SELECT * FROM tareas ORDER BY creada_en DESC')

    # fetchall() recupera TODAS las filas del resultado en una lista.
    tareas = cursor.fetchall()
    db.close()

    # Pasa la lista al template; se accede como variable {{ tareas }} en Jinja2.
    return render_template('index.html', tareas=tareas)


# ── UPDATE — Editar tarea ──────────────────────────────────────
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    """
    <int:id> en la ruta es un parámetro de URL.
    Flask lo convierte automáticamente a entero y lo pasa como
    argumento a la función.

    GET  → busca la tarea en la BD y muestra el formulario pre-rellenado.
    POST → actualiza los campos en la BD y redirige al listado.
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form.get('descripcion', '')

        # Los checkboxes HTML solo se envían en el formulario cuando están
        # marcados. Si no está marcado, 'completada' no aparece en request.form.
        # El operador 'in' devuelve True si existe la clave, False si no.
        completada = 'completada' in request.form

        # UPDATE modifica solo la fila cuyo id coincide con el parámetro de URL.
        # El WHERE id=%s es crítico: sin él se actualizarían TODAS las filas.
        cursor.execute(
            'UPDATE tareas SET titulo=%s, descripcion=%s, completada=%s WHERE id=%s',
            (titulo, descripcion, completada, id)
        )
        db.commit()
        db.close()
        return redirect(url_for('inicio'))

    # GET: obtiene los datos actuales de la tarea para pre-rellenar el formulario.
    # (id,) es una tupla de un elemento; la coma es obligatoria en Python
    # para que no se interprete como un simple paréntesis.
    cursor.execute('SELECT * FROM tareas WHERE id=%s', (id,))
    tarea = cursor.fetchone()  # fetchone() devuelve solo una fila (o None)
    db.close()

    # Pasa el dict de la tarea a la plantilla editar.html.
    return render_template('editar.html', tarea=tarea)


# ── DELETE — Eliminar tarea ────────────────────────────────────
@app.route('/eliminar/<int:id>')
def eliminar(id):
    """
    Elimina permanentemente la tarea con el id indicado en la URL.
    No tiene confirmación en el servidor (el botón de la vista
    podría agregar un confirm() de JavaScript como mejora futura).
    """
    db = get_db()
    cursor = db.cursor()

    # DELETE borra la fila cuyo id coincide. El WHERE es imprescindible.
    cursor.execute('DELETE FROM tareas WHERE id=%s', (id,))
    db.commit()
    db.close()

    return redirect(url_for('inicio'))


# ── Punto de entrada ───────────────────────────────────────────
if __name__ == '__main__':
    # debug=True activa el recargado automático al guardar archivos
    # y muestra mensajes de error detallados en el navegador.
    # NUNCA usar debug=True en producción.
    app.run(debug=True)
