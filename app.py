from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="veterinaria"
)

cursor = conexion.cursor(dictionary=True)


# =========================================================
# INICIO - LISTA DE ANIMALES
# =========================================================

@app.route('/')
def index():

    cursor.execute("""
        SELECT
            animales.id_animal,
            animales.nombre,
            animales.especie,
            animales.raza,
            animales.fecha_nacimiento,
            duenios.nombre AS duenio
        FROM animales
        JOIN duenios
            ON animales.id_duenio = duenios.id_duenio
        ORDER BY animales.nombre ASC
    """)

    animales = cursor.fetchall()

    return render_template(
        'index.html',
        animales=animales
    )


# =========================================================
# AGREGAR ANIMAL
# =========================================================

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():

    if request.method == 'POST':

        nombre = request.form['nombre']
        especie = request.form['especie']
        raza = request.form['raza']
        fecha_nacimiento = request.form['fecha_nacimiento']
        id_duenio = request.form['id_duenio']

        cursor.execute("""
            INSERT INTO animales
            (nombre, especie, raza, fecha_nacimiento, id_duenio)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            nombre,
            especie,
            raza,
            fecha_nacimiento,
            id_duenio
        ))

        conexion.commit()

        return redirect('/')

    cursor.execute("""
        SELECT *
        FROM duenios
        ORDER BY nombre ASC
    """)

    duenios = cursor.fetchall()

    return render_template(
        'agregar.html',
        duenios=duenios
    )


# =========================================================
# AGREGAR DUEÑO
# =========================================================

@app.route('/agregar-duenio', methods=['GET', 'POST'])
def agregar_duenio():

    if request.method == 'POST':

        nombre = request.form['nombre'].strip()
        rut = request.form['rut'].strip()
        telefono = request.form['telefono'].strip()
        correo = request.form['correo'].strip()
        direccion = request.form['direccion'].strip()

        if not nombre:

            return render_template(
                'agregar_duenio.html',
                error='El nombre del dueño es obligatorio.',
                nombre=nombre,
                rut=rut,
                telefono=telefono,
                correo=correo,
                direccion=direccion
            )

        cursor.execute(
            """
            SELECT id_duenio
            FROM duenios
            WHERE nombre = %s AND rut = %s
            """,
            (nombre, rut)
        )

        duenio_existente = cursor.fetchone()

        if duenio_existente:

            return render_template(
                'agregar_duenio.html',
                error='Este dueño ya se encuentra registrado.',
                nombre=nombre,
                rut=rut,
                telefono=telefono,
                correo=correo,
                direccion=direccion
            )

        cursor.execute("""
            INSERT INTO duenios
            (nombre, rut, telefono, correo, direccion)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            nombre,
            rut,
            telefono,
            correo,
            direccion
        ))

        conexion.commit()

        return redirect('/agregar')

    return render_template('agregar_duenio.html')


# =========================================================
# LISTA DE DUEÑOS
# =========================================================

@app.route('/duenios')
def duenios():

    cursor.execute("""
        SELECT
            duenios.id_duenio,
            duenios.nombre,
            duenios.rut,
            duenios.telefono,
            duenios.correo,
            duenios.direccion,
            COUNT(animales.id_animal) AS cantidad_animales
        FROM duenios
        LEFT JOIN animales
            ON duenios.id_duenio = animales.id_duenio
        GROUP BY
            duenios.id_duenio,
            duenios.nombre,
            duenios.rut,
            duenios.telefono,
            duenios.correo,
            duenios.direccion
        ORDER BY duenios.nombre ASC
    """)

    duenios = cursor.fetchall()

    return render_template(
        'duenios.html',
        duenios=duenios
    )


# =========================================================
# EDITAR ANIMAL
# =========================================================

@app.route('/editar/<int:id_animal>', methods=['GET', 'POST'])
def editar(id_animal):

    if request.method == 'POST':

        nombre = request.form['nombre']
        especie = request.form['especie']
        raza = request.form['raza']
        fecha_nacimiento = request.form['fecha_nacimiento']
        id_duenio = request.form['id_duenio']

        cursor.execute("""
            UPDATE animales
            SET
                nombre = %s,
                especie = %s,
                raza = %s,
                fecha_nacimiento = %s,
                id_duenio = %s
            WHERE id_animal = %s
        """, (
            nombre,
            especie,
            raza,
            fecha_nacimiento,
            id_duenio,
            id_animal
        ))

        conexion.commit()

        return redirect('/')

    cursor.execute("""
        SELECT
            id_animal,
            nombre,
            especie,
            raza,
            fecha_nacimiento,
            id_duenio
        FROM animales
        WHERE id_animal = %s
    """, (id_animal,))

    animal = cursor.fetchone()

    if not animal:
        return redirect('/')

    cursor.execute("""
        SELECT
            id_duenio,
            nombre
        FROM duenios
        ORDER BY nombre ASC
    """)

    duenios = cursor.fetchall()

    return render_template(
        'editar.html',
        animal=animal,
        duenios=duenios
    )


# =========================================================
# ELIMINAR ANIMAL
# =========================================================

@app.route('/eliminar/<int:id_animal>')
def eliminar(id_animal):

    cursor.execute(
        """
        DELETE FROM animales
        WHERE id_animal = %s
        """,
        (id_animal,)
    )

    conexion.commit()

    return redirect('/')


# =========================================================
# VER INFORMACIÓN DE UN ANIMAL
# =========================================================

@app.route('/consulta/<int:id_animal>')
def consulta(id_animal):

    cursor.execute("""
        SELECT
            animales.id_animal,
            animales.nombre,
            animales.especie,
            animales.raza,
            animales.fecha_nacimiento,
            duenios.nombre AS duenio
        FROM animales
        JOIN duenios
            ON animales.id_duenio = duenios.id_duenio
        WHERE animales.id_animal = %s
    """, (id_animal,))

    animal = cursor.fetchone()

    if not animal:
        return redirect('/')

    return render_template(
        'consulta.html',
        animal=animal
    )


# =========================================================
# LISTA DE CONSULTAS
# =========================================================

@app.route('/consultas')
def consultas():

    cursor.execute("""
        SELECT
            consultas.id_consulta,
            consultas.id_veterinario,
            consultas.id_animal,
            consultas.fecha,
            consultas.hora,
            consultas.motivo,
            animales.nombre AS animal
        FROM consultas
        JOIN animales
            ON consultas.id_animal = animales.id_animal
        ORDER BY consultas.fecha DESC, consultas.hora DESC
    """)

    consultas = cursor.fetchall()

    return render_template(
        'consultas.html',
        consultas=consultas
    )


# =========================================================
# NUEVA CONSULTA
# =========================================================

@app.route('/nueva-consulta', methods=['GET', 'POST'])
def nueva_consulta():

    # -----------------------------------------
    # GUARDAR CONSULTA
    # -----------------------------------------

    if request.method == 'POST':

        id_veterinario = request.form['id_veterinario']
        id_animal = request.form['id_animal']
        fecha = request.form['fecha']
        hora = request.form['hora']
        motivo = request.form['motivo'].strip()

        cursor.execute("""
            INSERT INTO consultas
            (
                id_veterinario,
                id_animal,
                fecha,
                hora,
                motivo
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            id_veterinario,
            id_animal,
            fecha,
            hora,
            motivo
        ))

        conexion.commit()

        return redirect('/consultas')

    # -----------------------------------------
    # CARGAR ANIMALES
    # -----------------------------------------

    cursor.execute("""
        SELECT
            animales.id_animal,
            animales.nombre,
            animales.especie,
            animales.raza,
            duenios.nombre AS duenio
        FROM animales
        JOIN duenios
            ON animales.id_duenio = duenios.id_duenio
        ORDER BY animales.nombre ASC
    """)

    animales = cursor.fetchall()

    return render_template(
        'nueva_consulta.html',
        animales=animales
    )


# =========================================================
# EJECUTAR APLICACIÓN
# =========================================================

if __name__ == '__main__':
    app.run(debug=True)