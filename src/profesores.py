import shutil
from tkinter import *
from tkinter import ttk, filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from dataBaseProfesores import DatabaseManagerProfesores
import os
import cv2


class ProfesoresApp:
    def __init__(self, db_manager):
        self.db_manager = db_manager

        self.app = Tk()
        self.app.title("Tutorias")
        self.app.geometry("900x700")
        self.app.configure(bg="#2C3E50")
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
        main_frame = Frame(self.app, bg="#2C3E50")
        main_frame.pack(fill=BOTH, expand=True)

        # Title
        title_label = Label(
            main_frame,
            text="REGISTRO DE PROFESORES",
            bg="#2C3E50",
            fg="#ECF0F1",
            font=("Helvetica", 28, "bold"),
            pady=20,
        )
        title_label.pack()

        input_frame = Frame(
            main_frame, bg="#34495E", bd=2, relief="groove", padx=20, pady=20
        )
        input_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

        self.create_input_fields(input_frame)

        self.create_buttons(input_frame)

        self.create_table(main_frame)

    def create_input_fields(self, frame):
        label_style = {
            "font": ("Helvetica", 12, "bold"),
            "bg": "#34495E",
            "fg": "#ECF0F1",
        }
        entry_style = {"font": ("Helvetica", 12), "bg": "#ECF0F1", "fg": "#2C3E50"}

        Label(frame, text="Codigo", **label_style).grid(
            column=0, row=0, padx=10, pady=10, sticky=Ee
        )
        Entry(frame, textvariable=self.Codigo, **entry_style).grid(
            column=1, row=0, padx=10, pady=10, sticky=W
        )

        Label(frame, text="Nombre", **label_style).grid(
            column=0, row=1, padx=10, pady=10, sticky=E
        )
        Entry(frame, textvariable=self.Nombre, **entry_style).grid(
            column=1, row=1, padx=10, pady=10, sticky=W
        )

        Label(frame, text="Apellido", **label_style).grid(
            column=0, row=2, padx=10, pady=10, sticky=E
        )
        Entry(frame, textvariable=self.Apellido, **entry_style).grid(
            column=1, row=2, padx=10, pady=10, sticky=W
        )

        Label(frame, text="Email", **label_style).grid(
            column=2, row=0, padx=10, pady=10, sticky=E
        )
        Entry(frame, textvariable=self.Email, **entry_style).grid(
            column=3, row=0, padx=10, pady=10, sticky=W
        )

        Label(frame, text="Genero", **label_style).grid(
            column=2, row=1, padx=10, pady=10, sticky=E
        )
        self.combox_genero = ttk.Combobox(
            frame, textvariable=self.Genero, state="readonly", font=("Helvetica", 12)
        )
        self.combox_genero["values"] = ("M", "F", "Otros")
        self.combox_genero.grid(column=3, row=1, padx=10, pady=10, sticky=W)

        Label(frame, text="Horario", **label_style).grid(
            column=2, row=2, padx=10, pady=10, sticky=E
        )
        self.combox_horario = ttk.Combobox(
            frame, textvariable=self.Horario, state="readonly", font=("Helvetica", 12)
        )
        self.combox_horario["values"] = ("Mañana", "Tarde", "Noche")
        self.combox_horario.grid(column=3, row=2, padx=10, pady=10, sticky=W)

    def create_buttons(self, frame):
        button_frame = Frame(frame, bg="#34495E")
        button_frame.grid(column=0, row=3, columnspan=4, pady=20)

        Button(
            button_frame,
            text="Mostrar",
            command=self.mostrar,
            font=("Helvetica", 12, "bold"),
            bg="#27AE60",
            fg="#ECF0F1",
            width=10,
            padx=5,
            pady=5,
            cursor="hand2",
        ).grid(column=0, row=0, padx=10)

        Button(
            button_frame,
            text="Insertar",
            command=self.insertar,
            font=("Helvetica", 12, "bold"),
            bg="#2980B9",
            fg="#ECF0F1",
            width=10,
            padx=5,
            pady=5,
            cursor="hand2",
        ).grid(column=1, row=0, padx=10)

        Button(
            button_frame,
            text="Eliminar",
            command=self.eliminar,
            font=("Helvetica", 12, "bold"),
            bg="#E74C3C",
            fg="#ECF0F1",
            width=10,
            padx=5,
            pady=5,
            cursor="hand2",
        ).grid(column=2, row=0, padx=10)

        Button(
            button_frame,
            text="Capturar Imagen",
            command=self.capturar_y_guardar_imagen,
            font=("Helvetica", 12, "bold"),
            bg="#8E44AD",
            fg="#ECF0F1",
            width=15,
            padx=5,
            pady=5,
            cursor="hand2",
        ).grid(column=3, row=0, padx=10)

    def create_table(self, frame):
        table_frame = Frame(frame, bg="#2C3E50")
        table_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

        style = ttk.Style()
        style.configure(
            "Treeview",
            background="#ECF0F1",
            foreground="#2C3E50",
            rowheight=25,
            fieldbackground="#ECF0F1",
        )
        style.map("Treeview", background=[("selected", "#2980B9")])

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
            self.tvProfesores.column(col, anchor=CENTER, width=120)
            self.tvProfesores.heading(col, text=col.capitalize(), anchor=CENTER)

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

    def capturar_y_guardar_imagen(self):
        # Obtener el nombre del usuario
        nombre_usuario = f"{self.Nombre.get()}_{self.Apellido.get()}"
        if not nombre_usuario or nombre_usuario == "_":
            messagebox.showerror(
                "Error",
                "Por favor, ingrese el nombre y apellido del profesor antes de capturar la imagen.",
            )
            return

        # Iniciar la cámara
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            messagebox.showerror("Error", "No se pudo acceder a la cámara.")
            return

        # Capturar imagen
        ret, frame = cap.read()

        if not ret:
            messagebox.showerror("Error", "No se pudo capturar la imagen.")
            cap.release()
            return

        # Liberar la cámara
        cap.release()

        # Convertir de BGR a RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Crear una imagen PIL
        img = Image.fromarray(rgb_frame)

        # Crear el directorio si no existe
        save_directory = os.path.join(os.getcwd(), "imagenes_profesores")
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # Guardar la imagen con el nombre del usuario
        img_path = os.path.join(save_directory, f"{nombre_usuario}.jpg")
        img.save(img_path)

        messagebox.showinfo("Éxito", f"Imagen guardada como {nombre_usuario}.jpg")


if __name__ == "__main__":
    db_manager = DatabaseManagerProfesores(
        host="localhost", user="root", password="123456789", database="tutoria"
    )
    app = ProfesoresApp(db_manager)
