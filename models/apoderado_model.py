from config import get_connection

def obtener_todos():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            apoderados.id_apoderado,
            apoderados.nombre,
            apoderados.rut,
            apoderados.telefono,
            apoderados.correo,
            apoderados.direccion,
            COUNT(alumnos.id_alumno) AS cantidad_alumnos
        FROM apoderados
        LEFT JOIN alumnos ON apoderados.id_apoderado = alumnos.id_apoderado
        GROUP BY apoderados.id_apoderado, apoderados.nombre, apoderados.rut, 
                 apoderados.telefono, apoderados.correo, apoderados.direccion
        ORDER BY apoderados.nombre ASC
    """)
    apoderados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return apoderados

def obtener_por_id(id_apoderado):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT id_apoderado, nombre, rut, telefono, correo, direccion
        FROM apoderados
        WHERE id_apoderado = %s
    """, (id_apoderado,))
    apoderado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return apoderado

def obtener_para_seleccion():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id_apoderado, nombre FROM apoderados ORDER BY nombre ASC")
    apoderados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return apoderados

def buscar_por_nombre_y_rut(nombre, rut):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT id_apoderado FROM apoderados WHERE nombre = %s AND rut = %s
    """, (nombre, rut))
    apoderado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return apoderado

def guardar(nombre, rut, telefono, correo, direccion):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO apoderados (nombre, rut, telefono, correo, direccion)
        VALUES (%s, %s, %s, %s, %s)
    """, (nombre, rut, telefono, correo, direccion))
    conexion.commit()
    cursor.close()
    conexion.close()

def actualizar(id_apoderado, nombre, rut, telefono, correo, direccion):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE apoderados
        SET nombre = %s, rut = %s, telefono = %s, correo = %s, direccion = %s
        WHERE id_apoderado = %s
    """, (nombre, rut, telefono, correo, direccion, id_apoderado))
    conexion.commit()
    cursor.close()
    conexion.close()

def eliminar(id_apoderado):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM apoderados WHERE id_apoderado = %s", (id_apoderado,))
    conexion.commit()
    cursor.close()
    conexion.close()