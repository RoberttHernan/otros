# Manual de Usuario — Gestor de Tareas con Flask y MySQL

> **Taller de Desarrollo Web con Python**
> Nivel: estudiantes con conocimientos básicos de Python y HTML.

---

## Tabla de contenidos

1. [¿Qué hace esta aplicación?](#1-qué-hace-esta-aplicación)
2. [Estructura del proyecto](#2-estructura-del-proyecto)
3. [Requisitos e instalación](#3-requisitos-e-instalación)
4. [Base de datos — `db.sql`](#4-base-de-datos--dbsql)
5. [Servidor web — `app.py`](#5-servidor-web--apppy)
6. [Plantillas HTML](#6-plantillas-html)
7. [Flujo completo de una petición](#7-flujo-completo-de-una-petición)
8. [Conceptos clave](#8-conceptos-clave)
9. [Cómo ejecutar el proyecto](#9-cómo-ejecutar-el-proyecto)
10. [Errores comunes](#10-errores-comunes)

---

## 1. ¿Qué hace esta aplicación?

Es un **gestor de tareas** (to-do list) con interfaz web. Permite:

| Operación | Descripción | Ruta |
|-----------|-------------|------|
| **Crear** | Agregar una nueva tarea | `/agregar` |
| **Leer** | Ver la lista de tareas | `/` |
| **Editar** | Modificar título, descripción o estado | `/editar/<id>` |
| **Eliminar** | Borrar una tarea permanentemente | `/eliminar/<id>` |

Estas cuatro operaciones se conocen como **CRUD** (Create, Read, Update, Delete) y son la base de casi cualquier aplicación web real.

---

## 2. Estructura del proyecto

```
Taller/
│
├── app.py              ← Lógica del servidor (rutas, conexión a BD)
├── db.sql              ← Script SQL para crear la base de datos
├── requirements.txt    ← Librerías de Python necesarias
│
└── templates/          ← Páginas HTML dinámicas (Jinja2)
    ├── base.html       ← Plantilla madre con nav, estilos y footer
    ├── index.html      ← Lista de tareas (hereda de base.html)
    ├── agregar.html    ← Formulario para crear tarea (hereda de base.html)
    └── editar.html     ← Formulario para editar tarea (hereda de base.html)
```

### ¿Por qué esta estructura?

- `app.py` separa la **lógica** del **diseño** (principio de separación de responsabilidades).
- La carpeta `templates/` agrupa todos los archivos HTML. Flask la busca automáticamente.
- `base.html` evita repetir el mismo `<nav>`, `<head>` y `<footer>` en cada página.

---

## 3. Requisitos e instalación

### `requirements.txt`

```
flask
mysql-connector-python
```

| Librería | Para qué sirve |
|----------|----------------|
| `flask` | Micro-framework web: maneja las rutas HTTP, renderiza plantillas y devuelve respuestas al navegador. |
| `mysql-connector-python` | Driver oficial de MySQL para Python. Abre conexiones, ejecuta sentencias SQL y devuelve resultados como listas de diccionarios. |

### Instalar las dependencias

```bash
pip install -r requirements.txt
```

> Este comando lee el archivo `requirements.txt` e instala cada librería listada. Es la forma estándar de compartir dependencias en proyectos Python.

---

## 4. Base de datos — `db.sql`

```sql
CREATE DATABASE IF NOT EXISTS taller_flask;
USE taller_flask;

CREATE TABLE IF NOT EXISTS tareas (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    titulo      VARCHAR(200) NOT NULL,
    descripcion TEXT,
    completada  BOOLEAN DEFAULT FALSE,
    creada_en   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Explicación columna por columna

| Columna | Tipo | Significado |
|---------|------|-------------|
| `id` | `INT AUTO_INCREMENT PRIMARY KEY` | Identificador único. MySQL lo incrementa solo con cada fila nueva. |
| `titulo` | `VARCHAR(200) NOT NULL` | Texto de máximo 200 caracteres. `NOT NULL` impide guardar una tarea sin título. |
| `descripcion` | `TEXT` | Texto largo sin límite fijo. Puede estar vacío (`NULL`). |
| `completada` | `BOOLEAN DEFAULT FALSE` | `0` = pendiente, `1` = completada. Empieza en `FALSE` (pendiente). |
| `creada_en` | `TIMESTAMP DEFAULT CURRENT_TIMESTAMP` | Fecha y hora de creación. MySQL la rellena automáticamente. |

### Cómo ejecutar el script

```bash
mysql -u root -p < db.sql
```

Este comando conecta a MySQL con el usuario `root`, pide la contraseña y ejecuta todo el SQL del archivo de una vez.

---

## 5. Servidor web — `app.py`

### 5.1 Importaciones y configuración

```python
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'tu_password',
    'database': 'taller_flask'
}
```

- `Flask(__name__)` — crea la aplicación. `__name__` es el nombre del módulo actual; Flask lo usa para saber dónde están los archivos del proyecto.
- `DB_CONFIG` — diccionario con los datos de conexión a MySQL. Cambia `user` y `password` por los de tu instalación.

### 5.2 Función `get_db()`

```python
def get_db():
    return mysql.connector.connect(**DB_CONFIG)
```

Abre una conexión nueva a MySQL y la devuelve. Se llama al inicio de cada ruta. El `**DB_CONFIG` desempaqueta el diccionario y pasa cada clave como argumento con nombre (equivale a escribir `host='localhost', user='root', ...`).

> **Importante:** cada vez que llamas a `get_db()` se abre una conexión. Siempre debes cerrarla con `db.close()` para no agotar los recursos del servidor.

---

### 5.3 Ruta CREATE — `/agregar`

```python
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form.get('descripcion', '')

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO tareas (titulo, descripcion) VALUES (%s, %s)',
            (titulo, descripcion)
        )
        db.commit()
        db.close()
        return redirect(url_for('inicio'))

    return render_template('agregar.html')
```

**¿Cómo funciona?**

1. `@app.route('/agregar', methods=['GET', 'POST'])` — registra la URL `/agregar` y acepta dos tipos de petición:
   - **GET**: el usuario abre la página → se muestra el formulario vacío.
   - **POST**: el usuario envió el formulario → se procesa y guarda.

2. `request.form['titulo']` — lee el campo `name="titulo"` del formulario HTML.

3. `%s` en el SQL — marcador de posición (placeholder). **Nunca se debe construir el SQL concatenando cadenas** porque permite ataques de SQL Injection. El driver reemplaza `%s` de forma segura.

4. `db.commit()` — confirma la transacción. Sin esto, el INSERT se descarta.

5. `redirect(url_for('inicio'))` — redirige al listado. `url_for('inicio')` genera la URL de la función `inicio()`, que es `/`.

---

### 5.4 Ruta READ — `/`

```python
@app.route('/')
def inicio():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tareas ORDER BY creada_en DESC')
    tareas = cursor.fetchall()
    db.close()
    return render_template('index.html', tareas=tareas)
```

**¿Cómo funciona?**

1. `cursor(dictionary=True)` — hace que cada fila sea un diccionario `{'id': 1, 'titulo': 'Estudiar', ...}` en lugar de una tupla `(1, 'Estudiar', ...)`. Así se puede usar `{{ tarea.titulo }}` en la plantilla.

2. `ORDER BY creada_en DESC` — ordena de más nueva a más antigua.

3. `fetchall()` — trae todas las filas del resultado como lista de dicts.

4. `render_template('index.html', tareas=tareas)` — renderiza la plantilla y le pasa la variable `tareas`. En Jinja2, esa variable queda disponible como `{{ tareas }}`.

---

### 5.5 Ruta UPDATE — `/editar/<int:id>`

```python
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form.get('descripcion', '')
        completada = 'completada' in request.form

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
```

**¿Cómo funciona?**

1. `<int:id>` — parámetro dinámico en la URL. Cuando el usuario visita `/editar/3`, Flask pasa `id=3` a la función automáticamente convertido a entero.

2. `completada = 'completada' in request.form` — los checkboxes HTML **solo aparecen en el formulario si están marcados**. Si el checkbox tiene `name="completada"` y está tildado, la clave `'completada'` existe en `request.form`. Si no está tildado, no existe. Por eso se usa `in` en lugar de `.get()`.

3. `WHERE id=%s` en el UPDATE — sin este `WHERE` se modificarían **todas** las filas de la tabla. Nunca omitirlo.

4. `fetchone()` — obtiene solo una fila. Se usa cuando esperamos un resultado único (buscar por clave primaria).

---

### 5.6 Ruta DELETE — `/eliminar/<int:id>`

```python
@app.route('/eliminar/<int:id>')
def eliminar(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM tareas WHERE id=%s', (id,))
    db.commit()
    db.close()
    return redirect(url_for('inicio'))
```

**¿Cómo funciona?**

1. No necesita `methods=` explícitos porque solo acepta GET (el usuario hace clic en un enlace).
2. `DELETE FROM tareas WHERE id=%s` — borra solo la fila con ese `id`.
3. Redirige al inicio. El usuario ve la lista actualizada sin la tarea eliminada.

---

## 6. Plantillas HTML

Las plantillas usan el motor **Jinja2**, que viene incluido con Flask. Permite mezclar HTML con lógica de Python usando etiquetas especiales.

| Sintaxis Jinja2 | Uso |
|-----------------|-----|
| `{{ variable }}` | Muestra el valor de una variable |
| `{% if condicion %}` | Condicional |
| `{% for item in lista %}` | Bucle |
| `{% extends 'base.html' %}` | Herencia de plantilla |
| `{% block nombre %}` | Define o rellena un bloque |

---

### 6.1 `base.html` — Plantilla madre

Define la estructura común: `<head>` con estilos, barra de navegación (`<nav>`), contenedor principal (`<main>`) y pie de página (`<footer>`).

```html
{% block contenido %}{% endblock %}
```

Este bloque vacío es el "hueco" que las páginas hijas rellenan con su contenido propio. No repetir nav/footer en cada archivo es el principio **DRY** (Don't Repeat Yourself).

**Estilos incluidos:** todo el CSS está incrustado en `<style>` dentro de `base.html`. Define componentes reutilizables:
- `.card` — tarjeta blanca con sombra.
- `.btn`, `.btn-primary`, `.btn-danger`, `.btn-secondary` — variantes de botones.
- `.badge-success`, `.badge-warning` — etiquetas de estado (verde/amarillo).
- `.form-group`, `input`, `textarea` — campos de formulario con foco azul.

---

### 6.2 `index.html` — Lista de tareas

```html
{% extends 'base.html' %}
{% block contenido %}
    {% if tareas %}
        <table>
            {% for tarea in tareas %}
            <tr>
                <td>{{ tarea.titulo }}</td>
                <td>
                    {% if tarea.completada %}
                        <span class='badge badge-success'>Completada</span>
                    {% else %}
                        <span class='badge badge-warning'>Pendiente</span>
                    {% endif %}
                </td>
                <td>
                    <a href='/editar/{{ tarea.id }}'>Editar</a>
                    <a href='/eliminar/{{ tarea.id }}'>Eliminar</a>
                </td>
            </tr>
            {% endfor %}
        </table>
    {% else %}
        <p>No tienes tareas registradas aún.</p>
    {% endif %}
{% endblock %}
```

- `{% if tareas %}` — si la lista está vacía muestra un mensaje de estado vacío en lugar de una tabla vacía.
- `{% for tarea in tareas %}` — itera la lista devuelta por `inicio()` en `app.py`.
- `tarea.completada` — accede al valor booleano para elegir el badge correcto.
- `href='/editar/{{ tarea.id }}'` — genera la URL con el id real, por ejemplo `/editar/3`.

---

### 6.3 `agregar.html` — Formulario de creación

```html
<form method='POST' action='/agregar'>
    <input type='text' name='titulo' required>
    <textarea name='descripcion'></textarea>
    <button type='submit'>Guardar Tarea</button>
</form>
```

- `method='POST'` — envía los datos en el cuerpo de la petición (no en la URL).
- `action='/agregar'` — URL a la que se envía el formulario.
- `name='titulo'` — debe coincidir exactamente con `request.form['titulo']` en `app.py`.
- `required` — validación del navegador: no deja enviar si el campo está vacío.

---

### 6.4 `editar.html` — Formulario de edición

```html
<form method='POST' action='/editar/{{ tarea.id }}'>
    <input type='text' name='titulo' value='{{ tarea.titulo }}'>
    <textarea name='descripcion'>{{ tarea.descripcion | default('') }}</textarea>
    <input type='checkbox' name='completada' {% if tarea.completada %}checked{% endif %}>
    <button type='submit'>Guardar Cambios</button>
</form>
```

Diferencias clave respecto a `agregar.html`:

| Elemento | En agregar | En editar |
|----------|-----------|-----------|
| `action` | `/agregar` | `/editar/{{ tarea.id }}` (incluye el id) |
| Campos | Vacíos | Pre-rellenados con los valores actuales |
| Checkbox estado | No existe | Existe, pre-marcado si ya estaba completada |

- `value='{{ tarea.titulo }}'` — pre-rellena el input con el valor actual.
- `{{ tarea.descripcion \| default('') }}` — el filtro `default('')` evita mostrar `None` si la descripción es nula en la BD.
- `{% if tarea.completada %}checked{% endif %}` — añade el atributo `checked` si la tarea ya estaba completada.

---

## 7. Flujo completo de una petición

### Ejemplo: editar la tarea con id 5

```
Navegador                   Flask (app.py)              MySQL
   │                             │                         │
   │── GET /editar/5 ──────────►│                         │
   │                             │── SELECT * WHERE id=5 ─►│
   │                             │◄── {id:5, titulo:...} ──│
   │◄── editar.html pre-relleno ─│                         │
   │                             │                         │
   │── POST /editar/5 ──────────►│                         │
   │   (titulo, descripcion,     │── UPDATE SET ... ───────►│
   │    completada)              │   WHERE id=5            │
   │                             │── db.commit() ──────────►│
   │◄── redirect → / ───────────│                         │
   │── GET / ─────────────────── ►│                         │
   │                             │── SELECT * ORDER BY ... ►│
   │◄── index.html actualizado ──│◄── [lista de tareas] ───│
```

---

## 8. Conceptos clave

### ¿Qué es un decorador `@app.route`?

```python
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    ...
```

El `@app.route(...)` le dice a Flask: *"cuando alguien visite la URL `/agregar`, llama a la función `agregar()`"*. Es la forma de **mapear URLs a funciones** en Flask.

### ¿Qué diferencia hay entre GET y POST?

| GET | POST |
|-----|------|
| Pide datos (leer) | Envía datos (crear/modificar) |
| Los parámetros van en la URL | Los datos van en el cuerpo de la petición |
| Se puede guardar en favoritos | No se puede repetir sin confirmación |
| Ejemplo: abrir una página | Ejemplo: enviar un formulario |

### ¿Por qué usar `%s` y no f-strings en SQL?

**Incorrecto (vulnerable):**
```python
cursor.execute(f"SELECT * FROM tareas WHERE id={id}")
```

Si `id` fuera `1 OR 1=1`, la consulta devolvería **todas las filas**. Esto se llama **SQL Injection** y es una de las vulnerabilidades más comunes y peligrosas.

**Correcto (seguro):**
```python
cursor.execute("SELECT * FROM tareas WHERE id=%s", (id,))
```

El driver escapa automáticamente el valor antes de enviarlo a MySQL, haciendo imposible la inyección.

### ¿Qué es Jinja2?

Motor de plantillas integrado en Flask. Permite insertar variables de Python en HTML de forma segura (también escapa caracteres especiales para evitar XSS). Los archivos `.html` en `templates/` son plantillas Jinja2.

---

## 9. Cómo ejecutar el proyecto

### Paso 1 — Preparar la base de datos

```bash
mysql -u root -p < db.sql
```

### Paso 2 — Configurar credenciales

Abre `app.py` y edita `DB_CONFIG`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'tu_usuario',      # ← cambia aquí
    'password': 'tu_password', # ← cambia aquí
    'database': 'taller_flask'
}
```

### Paso 3 — Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4 — Arrancar el servidor

```bash
python app.py
```

Deberías ver:

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Paso 5 — Abrir en el navegador

Visita [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 10. Errores comunes

| Error | Causa probable | Solución |
|-------|---------------|----------|
| `Access denied for user 'root'` | Contraseña incorrecta en `DB_CONFIG` | Verifica `user` y `password` |
| `Unknown database 'taller_flask'` | No se ejecutó `db.sql` | Ejecutar `mysql -u root -p < db.sql` |
| `ModuleNotFoundError: flask` | Dependencias no instaladas | `pip install -r requirements.txt` |
| `TemplateNotFound: editar.html` | El archivo no existe en `templates/` | Verificar que `editar.html` está en la carpeta `templates/` |
| Página en blanco / 500 Internal Error | Error en Python | Ver la consola donde ejecutaste `python app.py` |
| Los cambios en el formulario no se guardan | Falta `db.commit()` | Verificar que `commit()` está después del `execute()` |

---

*Manual generado para el Taller de Desarrollo Web con Python — 2025*
