from flask import Blueprint, render_template, request, redirect, url_for
import models.alumno_model as alumno_model
import models.apoderado_model as apoderado_model

alumno_bp = Blueprint('alumno', __name__)

@alumno_bp.route('/')
@alumno_bp.route('/alumnos')
def index():
    alumnos = alumno_model.obtener_todos()
    return render_template('alumno/index.html', alumnos=alumnos)

@alumno_bp.route('/alumno/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        rut = request.form['rut'].strip()
        curso = request.form['curso'].strip()
        fecha_nacimiento = request.form['fecha_nacimiento']
        id_apoderado = request.form['id_apoderado']

        alumno_model.guardar(nombre, rut, curso, fecha_nacimiento, id_apoderado)
        return redirect(url_for('alumno.index'))

    apoderados = apoderado_model.obtener_para_seleccion()
    return render_template('alumno/crear.html', apoderados=apoderados)

@alumno_bp.route('/alumno/editar/<int:id_alumno>', methods=['GET', 'POST'])
def editar(id_alumno):
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        rut = request.form['rut'].strip()
        curso = request.form['curso'].strip()
        fecha_nacimiento = request.form['fecha_nacimiento']
        id_apoderado = request.form['id_apoderado']

        alumno_model.actualizar(id_alumno, nombre, rut, curso, fecha_nacimiento, id_apoderado)
        return redirect(url_for('alumno.index'))

    alumno = alumno_model.obtener_por_id(id_alumno)
    if not alumno:
        return redirect(url_for('alumno.index'))

    apoderados = apoderado_model.obtener_para_seleccion()
    return render_template('alumno/editar.html', alumno=alumno, apoderados=apoderados)

@alumno_bp.route('/alumno/eliminar/<int:id_alumno>')
def eliminar(id_alumno):
    alumno_model.eliminar(id_alumno)
    return redirect(url_for('alumno.index'))