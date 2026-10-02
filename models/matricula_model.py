from config import get_connection

def obtener_todas():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            matriculas.id_matricula,
            matriculas.fecha_matricula,
            matriculas.anio_lectivo,
            matriculas.observaciones,
            alumnos.nombre AS alumno,
            alumnos.curso
        FROM matriculas
        JOIN alumnos ON matriculas.id_alumno = alumnos.id_alumno
        ORDER BY matriculas.fecha_matricula DESC
    """)
    matriculas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return matriculas

def obtener_por_id(id_matricula):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT id_matricula, id_alumno, fecha_matricula, anio_lectivo, observaciones
        FROM matriculas
        WHERE id_matricula = %s
    """, (id_matricula,))
    matricula = cursor.fetchone()
    cursor.close()
    conexion.close()
    return matricula

def guardar(id_alumno, fecha_matricula, anio_lectivo, observaciones):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO matriculas (id_alumno, fecha_matricula, anio_lectivo, observaciones)
        VALUES (%s, %s, %s, %s)
    """, (id_alumno, fecha_matricula, anio_lectivo, observaciones))
    conexion.commit()
    cursor.close()
    conexion.close()

def actualizar(id_matricula, id_alumno, fecha_matricula, anio_lectivo, observaciones):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE matriculas
        SET id_alumno = %s, fecha_matricula = %s, anio_lectivo = %s, observaciones = %s
        WHERE id_matricula = %s
    """, (id_alumno, fecha_matricula, anio_lectivo, observaciones, id_matricula))
    conexion.commit()
    cursor.close()
    conexion.close()

def eliminar(id_matricula):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM matriculas WHERE id_matricula = %s", (id_matricula,))
    conexion.commit()
    cursor.close()
    conexion.close()