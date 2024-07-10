from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from dataBaseAlumno import DatabaseManagerAlumno
from dataBaseProfesores import DatabaseManagerProfesores
from profesores import ProfesoresApp
from components.config import create_gui
import random


class AlumnoApp:
    def __init__(self, database_manager):
        self.database_manager = database_manager
        self.app = Tk()
        self.app.title("Alumno")
        self.app.geometry("900x700")

        self.icon_img = PhotoImage(
            file="./example/UNAS.png"
        )  # Reemplaza con la ruta de tu ícono
        self.app.iconphoto(False, self.icon_img)
        self.Codigo = StringVar()
        self.nombre_estudiante = StringVar()
        self.apellido_estudiante = StringVar()
        self.ciclo = StringVar()
        self.email = StringVar()
        self.telefono = StringVar()
        self.selecion_tutor = StringVar()
        self.create_widgets()
        self.app.mainloop()

    def create_widgets(self):
        main_frame = Frame(self.app, bg="#E8F0F2")
        main_frame.pack(fill=BOTH, expand=True)

        # Title
        title_label = Label(
            main_frame,
            text="REGISTRO DE ALUMNOS",
            bg="#E8F0F2",
            fg="#333333",
            font=("Helvetica", 24, "bold"),
            pady=20,
        )
        title_label.pack()

        input_frame = Frame(
            main_frame, bg="#FFFFFF", bd=2, relief="groove", padx=20, pady=20
        )
        input_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

        self.create_input_fields(input_frame)
        self.create_table(main_frame)
        self.create_buttons(input_frame)

    def create_input_fields(self, frame):
        Label(frame, text="Codigo", font=("Helvetica", 12), bg="#FFFFFF").grid(
            column=0, row=0, padx=10, pady=10, sticky=E
        )
        Entry(frame, textvariable=self.Codigo, font=("Helvetica", 12)).grid(
            column=1, row=0, padx=10, pady=10, sticky=W
        )

        Label(frame, text="Nombre", font=("Helvetica", 12), bg="#FFFFFF").grid(
            column=0, row=1, padx=10, pady=10, sticky=E
        )
        Entry(frame, textvariable=self.nombre_estudiante, font=("Helvetica", 12)).grid(
            column=1, row=1, padx=10, pady=10, sticky=W
        )

        Label(frame, text="Apellido", font=("Helvetica", 12), bg="#FFFFFF").grid(
            column=0, row=2, padx=10, pady=10, sticky=E
        )
        Entry(
            frame, textvariable=self.apellido_estudiante, font=("Helvetica", 12)
        ).grid(column=1, row=2, padx=10, pady=10, sticky=W)

        Label(frame, text="Ciclo", font=("Helvetica", 12), bg="#FFFFFF").grid(
            column=2, row=0, padx=10, pady=10, sticky=W
        )
        Entry(frame, textvariable=self.ciclo, font=("Helvetica", 12)).grid(
            column=3, row=0, padx=10, pady=10, sticky=E
        )

        Label(frame, text="Email", font=("Helvetica", 12), bg="#FFFFFF").grid(
            column=2, row=1, padx=10, pady=10, sticky=W
        )
        Entry(frame, textvariable=self.email, font=("Helvetica", 12)).grid(
            column=3, row=1, padx=10, pady=10, sticky=E
        )

        Label(frame, text="Telefono", font=("Helvetica", 12), bg="#FFFFFF").grid(
            column=2, row=2, padx=10, pady=10, sticky=W
        )
        Entry(frame, textvariable=self.telefono, font=("Helvetica", 12)).grid(
            column=3, row=2, padx=10, pady=10, sticky=E
        )

    def create_table(self, frame):
        table_frame = Frame(frame, bg="#E8F0F2")
        table_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

        self.tvAlumnos = ttk.Treeview(
            table_frame,
            columns=(
                "id_profesor",
                "Codigo",
                "Nombre",
                "Apellido",
                "Email",
                "Genero",
                "Horario",
            ),
            show="headings",
            selectmode="browse",
        )
        self.tvAlumnos.pack(fill=BOTH, expand=True)

        for col in (
            "id_profesor",
            "Codigo",
            "Nombre",
            "Apellido",
            "Email",
            "Genero",
            "Horario",
        ):
            self.tvAlumnos.column(col, anchor=CENTER, width=100)
            self.tvAlumnos.heading(col, text=col.capitalize())

    def create_buttons(self, frame):
        Button(
            frame, text="Registrar", font=("Helvetica", 12), command=self.registrar
        ).grid(column=0, row=3, padx=10, pady=10)
        Button(frame, text="Mostrar", font=("Helvetica", 12), command=self.show).grid(
            column=1, row=3, padx=10, pady=10
        )

        Button(
            frame,
            text="Asignar Mejores Tutores",
            font=("Helvetica", 12),
            command=self.asignar_mejores_tutores,
        ).grid(column=4, row=3, padx=10, pady=10)

        Button(
            frame,
            text="Tomar Foto",
            font=("Helvetica", 12),
            command=create_gui,
        ).grid(column=5, row=3, padx=10, pady=10)

    def registrar(self):
        data = (
            self.Codigo.get(),
            self.Nombre.get(),
            self.Apellido.get(),
            self.Email.get(),
            self.Genero.get(),
            self.Horario.get(),
        )
        self.database_manager.insert(data)
        self.mostrar()
        self.limpiar_campos()

    def show(self):
        for row in self.tvProfesores.get_children():
            self.tvProfesores.delete(row)
        rows = self.db_manager.fetch_all()
        for row in rows:
            self.tvProfesores.insert("", "end", values=row)

    def delete(self):
        selected_item = self
        if not selected_item:
            messagebox.showwarning(
                "Advertencia", "Debe seleccionar un elemento para eliminar."
            )
            return

        item = self.tvProfesores.item(selected_item)
        id_alumno = item["values"][0]
        self.db_manager.delete(id_alumno)
        self.mostrar()

    def asignar_mejores_tutores(self):
        # Obtener todos los alumnos
        alumnos = self.Codigo.get()

        # Obtener los mejores tutores (asumimos que hay un método para esto)
        mejores_tutores = DatabaseManagerProfesores.fetch_all(self.database_manager)

        if not mejores_tutores:
            messagebox.showinfo("Información", "No hay tutores disponibles.")
            return

        asignaciones = []

        for alumno in alumnos:
            # Seleccionar un tutor al azar de entre los mejores
            tutor = random.choice(mejores_tutores)

            # Crear la asignación
            asignacion = (alumno[0], tutor[0])  # (id_alumno, id_tutor)
            asignaciones.append(asignacion)

        # Guardar las asignaciones en la base de datos
        self.database_manager.guardar_asignaciones(asignaciones)

        messagebox.showinfo(
            "Éxito", "Se han asignado los mejores tutores a los alumnos."
        )

        # Actualizar la vista de la tabla
        self.mostrar()


if __name__ == "__main__":
    db_manager = DatabaseManagerAlumno(
        host="localhost", user="root", password="123456789", database="tutoria"
    )
    app = AlumnoApp(db_manager)
