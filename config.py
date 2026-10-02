import mysql.connector

def get_connection():
    """
    Establece y retorna una conexión a la base de datos MySQL del colegio.
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="colegio_db"
    )