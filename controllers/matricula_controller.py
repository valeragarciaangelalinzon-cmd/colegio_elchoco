from flask import Blueprint, render_template, request, redirect, url_for
import models.matricula_model as matricula_model
import models.alumno_model as alumno_model

matricula_bp = Blueprint('matricula', __name__)

@matricula_bp.route('/matriculas')
def index():
    matriculas = matricula_model.obtener_todas()
    return render_template('matricula/index.html', matriculas=matriculas)

@matricula_bp.route('/matricula/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        id_alumno = request.form['id_alumno']
        fecha_matricula = request.form['fecha_matricula']
        anio_lectivo = request.form['anio_lectivo']
        observaciones = request.form['observaciones'].strip()

        matricula_model.guardar(id_alumno, fecha_matricula, anio_lectivo, observaciones)
        return redirect(url_for('matricula.index'))

    alumnos = alumno_model.obtener_todos()
    return render_template('matricula/crear.html', alumnos=alumnos)

@matricula_bp.route('/matricula/editar/<int:id_matricula>', methods=['GET', 'POST'])
def editar(id_matricula):
    if request.method == 'POST':
        id_alumno = request.form['id_alumno']
        fecha_matricula = request.form['fecha_matricula']
        anio_lectivo = request.form['anio_lectivo']
        observaciones = request.form['observaciones'].strip()

        matricula_model.actualizar(id_matricula, id_alumno, fecha_matricula, anio_lectivo, observaciones)
        return redirect(url_for('matricula.index'))

    matricula = matricula_model.obtener_por_id(id_matricula)
    if not matricula:
        return redirect(url_for('matricula.index'))

    alumnos = alumno_model.obtener_todos()
    return render_template('matricula/editar.html', matricula=matricula, alumnos=alumnos)

@matricula_bp.route('/matricula/eliminar/<int:id_matricula>')
def eliminar(id_matricula):
    matricula_model.eliminar(id_matricula)
    return redirect(url_for('matricula.index'))