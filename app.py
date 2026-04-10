# app.py — versión con MySQL
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
 
app = Flask(__name__)
 
# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',          # cambia por tu usuario
    'password': 'tu_password',   # cambia por tu contraseña
    'database': 'taller'
}
 
def get_db():
    """Crea y devuelve una conexión a MySQL"""
    return mysql.connector.connect(**DB_CONFIG)
 
# ── CREATE ────────────────────────────────────────
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form.get('descripcion', '')
 
        db = get_db()
        cursor = db.cursor()
        # %s es el placeholder seguro (evita SQL Injection)
        cursor.execute(
            'INSERT INTO tareas (titulo, descripcion) VALUES (%s, %s)',
            (titulo, descripcion)
        )
        db.commit()   # confirmar el cambio
        db.close()
        return redirect(url_for('inicio'))
 
    return render_template('agregar.html')
 
# ── READ ──────────────────────────────────────────
@app.route('/')

def inicio():
    db = get_db()
    cursor = db.cursor(dictionary=True)  # devuelve dicts en lugar de tuplas
    cursor.execute('SELECT * FROM tareas ORDER BY creada_en DESC')
    tareas = cursor.fetchall()
    db.close()
    return render_template('index.html', tareas=tareas)
 
# ── UPDATE ────────────────────────────────────────
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
 
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form.get('descripcion', '')
        completada = 'completada' in request.form  # checkbox
        cursor.execute(
            'UPDATE tareas SET titulo=%s, descripcion=%s, completada=%s WHERE id=%s',
            (titulo, descripcion, completada, id)
        )
        db.commit()
        db.close()
        return redirect(url_for('inicio'))
 
    cursor.execute('SELECT * FROM tareas WHERE id=%s', (id,))
    tarea = cursor.fetchone()
    db.close()
    return render_template('editar.html', tarea=tarea)
 
# ── DELETE ────────────────────────────────────────
@app.route('/eliminar/<int:id>')
def eliminar(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM tareas WHERE id=%s', (id,))
    db.commit()
    db.close()
    return redirect(url_for('inicio'))
 
if __name__ == '__main__':
    app.run(debug=True)

