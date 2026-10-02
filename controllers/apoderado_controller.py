from flask import Blueprint, render_template, request, redirect, url_for
import models.apoderado_model as apoderado_model

apoderado_bp = Blueprint('apoderado', __name__)

@apoderado_bp.route('/apoderados')
def index():
    apoderados = apoderado_model.obtener_todos()
    return render_template('apoderado/index.html', apoderados=apoderados)

@apoderado_bp.route('/apoderado/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        rut = request.form['rut'].strip()
        telefono = request.form['telefono'].strip()
        correo = request.form['correo'].strip()
        direccion = request.form['direccion'].strip()

        if not nombre or not rut:
            return render_template('apoderado/crear.html', error='Nombre y RUT son obligatorios.')

        if apoderado_model.buscar_por_nombre_y_rut(nombre, rut):
            return render_template('apoderado/crear.html', error='Este apoderado ya se encuentra registrado.')

        apoderado_model.guardar(nombre, rut, telefono, correo, direccion)
        return redirect(url_for('apoderado.index'))

    return render_template('apoderado/crear.html')

@apoderado_bp.route('/apoderado/editar/<int:id_apoderado>', methods=['GET', 'POST'])
def editar(id_apoderado):
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        rut = request.form['rut'].strip()
        telefono = request.form['telefono'].strip()
        correo = request.form['correo'].strip()
        direccion = request.form['direccion'].strip()

        apoderado_model.actualizar(id_apoderado, nombre, rut, telefono, correo, direccion)
        return redirect(url_for('apoderado.index'))

    apoderado = apoderado_model.obtener_por_id(id_apoderado)
    if not apoderado:
        return redirect(url_for('apoderado.index'))

    return render_template('apoderado/editar.html', apoderado=apoderado)

@apoderado_bp.route('/apoderado/eliminar/<int:id_apoderado>')
def eliminar(id_apoderado):
    apoderado_model.eliminar(id_apoderado)
    return redirect(url_for('apoderado.index'))