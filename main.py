from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector


class ProfesoresApp:
    # Crean la entrada a la aplicacion y declaracion de la variables
    def __init__(self):
        self.app = Tk()
        self.app.title("Tutorias")
        self.app.geometry("700x600")

        self.id_profesor = IntVar()
        self.Codigo = StringVar()
        self.Nombre = StringVar()
        self.Apellido = StringVar()
        self.Email = StringVar()
        self.Genero = StringVar()
        self.Horario = StringVar()

        self.create_widgets()
        self.app.mainloop()

    def create_widgets(self):
        marco = LabelFrame(self.app, text="Seleccion de tutoria", bg="lightblue")
        marco.place(x=15, y=15, width=750, height=500)

        Label(marco, text="Codigo").grid(column=0, row=0, padx=5, pady=5)
        Entry(marco, textvariable=self.Codigo).grid(column=1, row=0, padx=5, pady=5)

        Label(marco, text="Nombre").grid(column=0, row=1, padx=5, pady=5)
        Entry(marco, textvariable=self.Nombre).grid(column=1, row=1, padx=5, pady=5)

        Label(marco, text="Apellido").grid(column=0, row=2, padx=5, pady=5)
        Entry(marco, textvariable=self.Apellido).grid(column=1, row=2, padx=5, pady=5)

        Label(marco, text="Email").grid(column=2, row=0, padx=5, pady=5)
        Entry(marco, textvariable=self.Email).grid(column=3, row=0, padx=5, pady=5)

        Label(marco, text="Genero").grid(column=2, row=1, padx=5, pady=5)
        Entry(marco, textvariable=self.Genero).grid(column=3, row=1, padx=5, pady=5)

        # Generar una opcion para el genero
        self.combox_genero = ttk.Combobox(marco, textvariable=self.Genero)
        self.combox_genero["values"] = ("M", "F", "Otros")
        self.combox_genero.grid(column=3, row=1, padx=3, pady=3)

        Label(marco, text="Horario").grid(column=2, row=2, padx=5, pady=5)
        Entry(marco, textvariable=self.Horario).grid(column=3, row=2, padx=5, pady=5)

        # Opciones de seleciones para el horario de la tutoria
        self.combox_horario = ttk.Combobox(marco, textvariable=self.Horario)
        self.combox_horario["values"] = ("Manana", "Tarde", "Noche")
        self.combox_horario.grid(column=3, row=2, padx=3, pady=3)

        Button(marco, text="Mostrar", command=lambda: self.mostrar()).grid(
            column=0, row=4, padx=10, pady=10
        )
        Button(marco, text="Insertar", command=lambda: self.insertar()).grid(
            column=1, row=4, padx=10, pady=10
        )
        Button(marco, text="Eliminar", command=lambda: self.eliminar()).grid(
            column=2, row=4, padx=10, pady=10
        )

        # Visualizar en una tabla la base de datos
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
        self.tvProfesores.grid(column=0, row=5, columnspan=5, padx=10, pady=10)
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

        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="123456789",
                database="hello_mysql",
            )
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM hello_mysql.profesores")

            for row in cursor:
                self.tvProfesores.insert("", "end", text=row[0], values=row)

            cursor.close()
            conexion.close()

        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Error al obtener datos: {error}")

    def insertar(self):

        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="123456789",
                database="hello_mysql",
            )
            cursor = conexion.cursor()

            sql = (
                "INSERT INTO hello_mysql.profesores (id_profesor, Codigo, Nombre, Apellido, Email, Genero, Horario) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            )

            id_profesor = self.id_profesor.get()
            Codigo = self.Codigo.get()
            Nombre = self.Nombre.get()
            Apellido = self.Apellido.get()
            Email = self.Email.get()
            Genero = self.Genero.get()
            Horario = self.Horario.get()

            values = (
                id_profesor,
                Codigo,
                Nombre,
                Apellido,
                Email,
                Genero,
                Horario,
            )

            cursor.execute(sql, values)
            conexion.commit()

        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Error al insertar datos: {error}")

    def eliminar(self):
        pass

    def limpiar_campos(self):
        self.Codigo.set("")
        self.Nombre.set("")
        self.Apellido.set("")
        self.Email.set("")
        self.Genero.set("")
        self.Horario.set("")


if __name__ == "__main__":
    app = ProfesoresApp()
