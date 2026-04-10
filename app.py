from flask import Flask, render_template, request, redirect, url_for
 
app = Flask(__name__)
 
# Lista temporal (sin base de datos todavía)
tareas_temp = []
 
@app.route('/')
def inicio():
    return render_template('index.html', tareas=tareas_temp)
 
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        # Leer los datos que envió el formulario
        titulo = request.form['titulo']
        descripcion = request.form.get('descripcion', '')
 
        # Agregar a la lista temporal
        tareas_temp.append({
            'id': len(tareas_temp) + 1,
            'titulo': titulo,
            'descripcion': descripcion,
            'completada': False
        })
 
        # Redirigir al inicio después de guardar
        return redirect(url_for('inicio'))
 
    # Si es GET, mostrar el formulario vacío
    return render_template('agregar.html')
 
if __name__ == '__main__':
    app.run(debug=True)



