from config import get_connection

def obtener_todos():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            alumnos.id_alumno,
            alumnos.nombre,
            alumnos.rut,
            alumnos.curso,
            alumnos.fecha_nacimiento,
            apoderados.nombre AS apoderado
        FROM alumnos
        JOIN apoderados ON alumnos.id_apoderado = apoderados.id_apoderado
        ORDER BY alumnos.nombre ASC
    """)
    alumnos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return alumnos

def obtener_por_id(id_alumno):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            alumnos.id_alumno,
            alumnos.nombre,
            alumnos.rut,
            alumnos.curso,
            alumnos.fecha_nacimiento,
            alumnos.id_apoderado,
            apoderados.nombre AS apoderado
        FROM alumnos
        JOIN apoderados ON alumnos.id_apoderado = apoderados.id_apoderado
        WHERE alumnos.id_alumno = %s
    """, (id_alumno,))
    alumno = cursor.fetchone()
    cursor.close()
    conexion.close()
    return alumno

def guardar(nombre, rut, curso, fecha_nacimiento, id_apoderado):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO alumnos (nombre, rut, curso, fecha_nacimiento, id_apoderado)
        VALUES (%s, %s, %s, %s, %s)
    """, (nombre, rut, curso, fecha_nacimiento, id_apoderado))
    conexion.commit()
    cursor.close()
    conexion.close()

def actualizar(id_alumno, nombre, rut, curso, fecha_nacimiento, id_apoderado):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE alumnos
        SET nombre = %s, rut = %s, curso = %s, fecha_nacimiento = %s, id_apoderado = %s
        WHERE id_alumno = %s
    """, (nombre, rut, curso, fecha_nacimiento, id_apoderado, id_alumno))
    conexion.commit()
    cursor.close()
    conexion.close()

def eliminar(id_alumno):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM alumnos WHERE id_alumno = %s", (id_alumno,))
    conexion.commit()
    cursor.close()
    conexion.close()