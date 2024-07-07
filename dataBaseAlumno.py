import mysql.connector
from tkinter import messagebox


class DatabaseManagerAlumno:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            database=self.database,
        )

    def fetch_all(self):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM tutoria.alumnos")
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            return rows
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Error al obtener datos: {error}")
            return []

    def insert(self, data):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            sql = (
                "INSERT INTO profesores (id_profesor,codigo_alumno, nombre_alumno, apellido_alumno, ciclo, email, telefono) "
                "VALUES (%s, %s, %s, %s, %s, %s)"
            )
            cursor.execute(sql, data)
            connection.commit()
            cursor.close()
            connection.close()
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Error al insertar datos: {error}")
    def delete(self, id_profesor):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM profesores WHERE id_alumno = %s", (id_profesor,)
            )
            connection.commit()

            # Restablecer el ID a 1
            cursor.execute("ALTER TABLE alumnos AUTO_INCREMENT = 1")
            connection.commit()

            cursor.close()
            connection.close()
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Error al eliminar datos: {error}")