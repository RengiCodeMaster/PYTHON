from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector


class DatabaseManager:
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
            cursor.execute("SELECT * FROM tutoria.profesores")
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
                "INSERT INTO profesores (codigo_profesor, nombre, apellido, email, genero, horario) "
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
                "DELETE FROM profesores WHERE id_profesor = %s", (id_profesor,)
            )
            connection.commit()
            cursor.close()
            connection.close()
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Error al eliminar datos: {error}")


class ProfesoresApp:
    def __init__(self, db_manager):
        self.db_manager = db_manager

        self.app = Tk()
        self.app.title("Tutorias")
        self.app.geometry("700x600")

        self.Codigo = StringVar()
        self.Nombre = StringVar()
        self.Apellido = StringVar()
        self.Email = StringVar()
        self.Genero = StringVar()
        self.Horario = StringVar()

        self.create_widgets()
        self.app.mainloop()

    def create_widgets(self):
        marco = LabelFrame(
            self.app,
            text="Seleccion de tutoria",
            bg="lightblue",
            font=("Arial", 16, "bold"),
        )
        marco.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(0, weight=1)

        Label(marco, text="Codigo", font=("Arial", 12)).grid(
            column=0, row=0, padx=10, pady=10, sticky=E
        )
        Entry(marco, textvariable=self.Codigo).grid(
            column=1, row=0, padx=10, pady=10, sticky=W
        )

        Label(marco, text="Nombre", font=("Arial", 12)).grid(
            column=0, row=1, padx=10, pady=10, sticky=E
        )
        Entry(marco, textvariable=self.Nombre).grid(
            column=1, row=1, padx=10, pady=10, sticky=W
        )

        Label(marco, text="Apellido", font=("Arial", 12)).grid(
            column=0, row=2, padx=10, pady=10, sticky=E
        )
        Entry(marco, textvariable=self.Apellido).grid(
            column=1, row=2, padx=10, pady=10, sticky=W
        )

        Label(marco, text="Email", font=("Arial", 12)).grid(
            column=2, row=0, padx=10, pady=10, sticky=E
        )
        Entry(marco, textvariable=self.Email).grid(
            column=3, row=0, padx=10, pady=10, sticky=W
        )

        Label(marco, text="Genero", font=("Arial", 12)).grid(
            column=2, row=1, padx=10, pady=10, sticky=E
        )
        self.combox_genero = ttk.Combobox(
            marco, textvariable=self.Genero, state="readonly"
        )
        self.combox_genero["values"] = ("M", "F", "Otros")
        self.combox_genero.grid(column=3, row=1, padx=5, pady=5, sticky=W)

        Label(marco, text="Horario", font=("Arial", 12)).grid(
            column=2, row=2, padx=10, pady=10, sticky=E
        )
        self.combox_horario = ttk.Combobox(
            marco, textvariable=self.Horario, state="readonly"
        )
        self.combox_horario["values"] = ("Mañana", "Tarde", "Noche")
        self.combox_horario.grid(column=3, row=2, padx=3, pady=3, sticky=W)

        Button(marco, text="Mostrar", command=self.mostrar, font=("Arial", 12)).grid(
            column=0, row=4, padx=25, pady=15, sticky=W
        )
        Button(marco, text="Insertar", command=self.insertar, font=("Arial", 12)).grid(
            column=1, row=4, padx=25, pady=15, sticky=W
        )
        Button(marco, text="Eliminar", command=self.eliminar, font=("Arial", 12)).grid(
            column=2, row=4, padx=25, pady=15, sticky=W
        )

        for i in range(8):
            marco.grid_rowconfigure(i, weight=1)
        for i in range(6):
            marco.grid_columnconfigure(i, weight=1)

        self.tvProfesores = ttk.Treeview(
            marco,
            columns=(
                "id_profesor",
                "Codigo",
                "Nombre",
                "Apellido",
                "Email",
                "Genero",
                "Horario",
            ),
        )
        self.tvProfesores.grid(
            column=0, row=5, columnspan=5, padx=10, pady=10, sticky="nsew"
        )
        self.tvProfesores["show"] = "headings"

        for col in (
            "id_profesor",
            "Codigo",
            "Nombre",
            "Apellido",
            "Email",
            "Genero",
            "Horario",
        ):
            self.tvProfesores.column(col, width=100, anchor="center")
            self.tvProfesores.heading(col, text=col.capitalize())

    def mostrar(self):
        for row in self.tvProfesores.get_children():
            self.tvProfesores.delete(row)

        rows = self.db_manager.fetch_all()
        for row in rows:
            self.tvProfesores.insert("", "end", text=row[0], values=row)

    def insertar(self):
        data = (
            self.Codigo.get(),
            self.Nombre.get(),
            self.Apellido.get(),
            self.Email.get(),
            self.Genero.get(),
            self.Horario.get(),
        )
        self.db_manager.insert(data)
        self.mostrar()
        self.limpiar_campos()

    def eliminar(self):
        selected_item = self.tvProfesores.selection()
        if not selected_item:
            messagebox.showwarning(
                "Advertencia", "Debe seleccionar un elemento para eliminar."
            )
            return

        item = self.tvProfesores.item(selected_item)
        id_profesor = item["values"][0]
        self.db_manager.delete(id_profesor)
        self.mostrar()

    def limpiar_campos(self):
        self.Codigo.set("")
        self.Nombre.set("")
        self.Apellido.set("")
        self.Email.set("")
        self.Genero.set("")
        self.Horario.set("")


if __name__ == "__main__":
    db_manager = DatabaseManager(
        host="localhost", user="root", password="123456789", database="tutoria"
    )
    app = ProfesoresApp(db_manager)
