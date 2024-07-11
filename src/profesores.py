from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from dataBaseProfesores import DatabaseManagerProfesores


class ProfesoresApp:
    def __init__(self, db_manager):
        self.db_manager = db_manager

        self.app = Tk()
        self.app.title("Tutorias")
        self.app.geometry("900x700")
        self.app.configure(bg="#E8F0F2")
        self.icon_img = PhotoImage(
            file="./example/UNAS.png"
        )  # Reemplaza con la ruta de tu ícono
        self.app.iconphoto(False, self.icon_img)
        self.Codigo = StringVar()
        self.Nombre = StringVar()
        self.Apellido = StringVar()
        self.Email = StringVar()
        self.Genero = StringVar()
        self.Horario = StringVar()

        self.create_widgets()
        self.app.mainloop()

    def create_widgets(self):
        main_frame = Frame(self.app, bg="#E8F0F2")
        main_frame.pack(fill=BOTH, expand=True)

        # Title
        title_label = Label(
            main_frame,
            text="REGISTRO DE PROFESORES",
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

        self.create_buttons(input_frame)

        self.create_table(main_frame)

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
        Entry(frame, textvariable=self.Nombre, font=("Helvetica", 12)).grid(
            column=1, row=1, padx=10, pady=10, sticky=W
        )

        Label(frame, text="Apellido", font=("Helvetica", 12), bg="#FFFFFF").grid(
            column=0, row=2, padx=10, pady=10, sticky=E
        )
        Entry(frame, textvariable=self.Apellido, font=("Helvetica", 12)).grid(
            column=1, row=2, padx=10, pady=10, sticky=W
        )

        Label(frame, text="Email", font=("Helvetica", 12), bg="#FFFFFF").grid(
            column=2, row=0, padx=10, pady=10, sticky=E
        )
        Entry(frame, textvariable=self.Email, font=("Helvetica", 12)).grid(
            column=3, row=0, padx=10, pady=10, sticky=W
        )

        Label(frame, text="Genero", font=("Helvetica", 12), bg="#FFFFFF").grid(
            column=2, row=1, padx=10, pady=10, sticky=E
        )
        self.combox_genero = ttk.Combobox(
            frame, textvariable=self.Genero, state="readonly", font=("Helvetica", 12)
        )
        self.combox_genero["values"] = ("M", "F", "Otros")
        self.combox_genero.grid(column=3, row=1, padx=10, pady=10, sticky=W)

        Label(frame, text="Horario", font=("Helvetica", 12), bg="#FFFFFF").grid(
            column=2, row=2, padx=10, pady=10, sticky=E
        )
        self.combox_horario = ttk.Combobox(
            frame, textvariable=self.Horario, state="readonly", font=("Helvetica", 12)
        )
        self.combox_horario["values"] = ("Mañana", "Tarde", "Noche")
        self.combox_horario.grid(column=3, row=2, padx=10, pady=10, sticky=W)

    def create_buttons(self, frame):
        button_frame = Frame(frame, bg="#FFFFFF")
        button_frame.grid(column=0, row=3, columnspan=4, pady=20)

        Button(
            button_frame,
            text="Mostrar",
            command=self.mostrar,
            font=("Helvetica", 12),
            bg="#19E329",
            fg="#FFFFFF",
            width=10,
            padx=5,
            pady=5,
            cursor="hand2",
        ).grid(column=0, row=0, padx=10)

        Button(
            button_frame,
            text="Insertar",
            command=self.insertar,
            font=("Helvetica", 12),
            bg="#1974E3",
            fg="#FFFFFF",
            width=10,
            padx=5,
            pady=5,
            cursor="hand2",
        ).grid(column=1, row=0, padx=10)

        Button(
            button_frame,
            text="Eliminar",
            command=self.eliminar,
            font=("Helvetica", 12),
            bg="#E32319",
            fg="#FFFFFF",
            width=10,
            padx=5,
            pady=5,
            cursor="hand2",
        ).grid(column=2, row=0, padx=10)

    def create_table(self, frame):
        table_frame = Frame(frame, bg="#E8F0F2")
        table_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

        self.tvProfesores = ttk.Treeview(
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
        self.tvProfesores.pack(fill=BOTH, expand=True)

        for col in (
            "id_profesor",
            "Codigo",
            "Nombre",
            "Apellido",
            "Email",
            "Genero",
            "Horario",
        ):
            self.tvProfesores.column(col, anchor=CENTER, width=100)
            self.tvProfesores.heading(col, text=col.capitalize())

    def mostrar(self):
        for row in self.tvProfesores.get_children():
            self.tvProfesores.delete(row)
        rows = self.db_manager.fetch_all()
        for row in rows:
            self.tvProfesores.insert("", "end", values=row)

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
    db_manager = DatabaseManagerProfesores(
        host="localhost", user="root", password="123456789", database="tutoria"
    )
    app = ProfesoresApp(db_manager)
