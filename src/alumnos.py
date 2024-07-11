from tkinter import *
from PIL import Image, ImageTk
import pymysql
import cv2
import numpy as np


class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.connection = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        self.cursor = self.connection.cursor()

    def insert_alumno(self, alumno_data):
        sql = "INSERT INTO alumnos (codigo, nombre, apellido, email, telefono, ciclo) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            self.cursor.execute(sql, alumno_data)
            self.connection.commit()
        except pymysql.Error as e:
            raise Exception(f"Database error: {e}")

    def fetch_all_alumnos(self):
        self.cursor.execute(
            "SELECT id_alumno, codigo, nombre, apellido, email, telefono, ciclo FROM alumnos"
        )
        return self.cursor.fetchall()

    def update_alumno(self, alumno_data):
        sql = "UPDATE alumnos SET codigo=%s, nombre=%s, apellido=%s, email=%s, telefono=%s, ciclo=%s WHERE id_alumno=%s"
        try:
            self.cursor.execute(sql, alumno_data)
            self.connection.commit()
        except pymysql.Error as e:
            raise Exception(f"Database error: {e}")

    def delete_alumno(self, alumno_id):
        try:
            self.cursor.execute("DELETE FROM alumnos WHERE id_alumno=%s", (alumno_id,))
            self.connection.commit()

        except pymysql.Error as e:
            raise Exception(f"Database error: {e}")

    def close(self):
        self.connection.close()


class AlumnoApp:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.root = Tk()
        self.root.title("Gestión de Alumnos")
        self.root.geometry("1200x800")
        self.create_widgets()
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def create_widgets(self):
        self.title_label = Label(
            self.root, text="Registro de Alumnos", font=("Roboto Medium", 16)
        )
        self.title_label.pack(pady=20)

        self.form_frame = Frame(self.root)
        self.form_frame.pack(pady=20, padx=20, fill="both", expand=True)

        fields = ["Código", "Nombre", "Apellido", "Email", "Teléfono", "Ciclo"]
        self.entries = {}
        for index, field in enumerate(fields):
            label = Label(self.form_frame, text=f"{field}:")
            label.grid(row=index, column=0, pady=10, padx=10, sticky="w")
            entry = Entry(self.form_frame, width=30)
            entry.grid(row=index, column=1, pady=10, padx=10, sticky="w")
            self.entries[field] = entry

        self.add_button = Button(
            self.form_frame, text="Registrar", command=self.registrar
        )
        self.update_button = Button(
            self.form_frame, text="Actualizar", command=self.actualizar
        )
        self.delete_button = Button(
            self.form_frame, text="Eliminar", command=self.eliminar
        )
        self.load_photo_button = Button(
            self.form_frame, text="Cargar Foto", command=self.cargar_foto
        )
        self.take_photo_button = Button(
            self.form_frame,
            text="Tomar y Detectar Foto",
            command=self.tomar_foto_y_detectar,
        )
        self.add_button.grid(row=7, column=0, pady=20)
        self.update_button.grid(row=7, column=1, pady=20)
        self.delete_button.grid(row=7, column=2, pady=20)
        self.load_photo_button.grid(row=7, column=3, pady=20)
        self.take_photo_button.grid(row=7, column=4, pady=20)

        self.photo_label = Label(self.form_frame)
        self.photo_label.grid(row=8, column=1, columnspan=2)

        self.table_frame = Frame(self.root)
        self.table_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.treeview = ttk.Treeview(
            self.table_frame, columns=("id",) + tuple(fields), show="headings"
        )
        for field in ("id",) + tuple(fields):
            self.treeview.heading(field, text=field)
            self.treeview.column(field, anchor="center", width=100)
        self.treeview.pack(pady=10, padx=10, fill="both", expand=True)
        self.treeview.bind("<ButtonRelease-1>", self.on_treeview_click)
        self.load_data()

    def cargar_foto(self):
        file_path = filedialog.askopenfilename(
            title="Selecciona una imagen",
            filetypes=[
                ("Image Files", "*.png;*.jpg;*.jpeg;*.bmp"),
                ("All Files", "*.*"),
            ],
        )
        if file_path:
            self.mostrar_imagen(file_path)

    def mostrar_imagen(self, file_path):
        img = Image.open(file_path)
        img = img.resize((200, 200), Image.ANTIALIAS)
        self.photo_image = ImageTk.PhotoImage(img)
        self.photo_label.configure(image=self.photo_image)
        self.photo_label.image = self.photo_image  # Mantener una referencia

    def tomar_foto_y_detectar(self):
        cap = cv2.VideoCapture(0)  # Intenta abrir la cámara 0
        if not cap.isOpened():
            messagebox.showerror("Error", "No se pudo acceder a la cámara")
            return  # Salir si no se puede abrir la cámara

        ret, frame = cap.read()
        cap.release()  # Asegurarse de liberar la cámara

        if not ret:
            messagebox.showerror("Error", "No se pudo capturar una imagen")
            return  # Salir si no se captura la imagen

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=4
        )

        if len(faces) == 0:
            messagebox.showinfo(
                "Resultado de la detección", "No se detectaron rostros."
            )
            return  # Salir si no se detectan rostros

        for x, y, w, h in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            rostro = frame[y : y + h, x : x + w]
            # Potencial implementación para verificar con la base de datos aquí

        # Convertir la imagen BGR a RGB para mostrar en Tkinter
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        img = img.resize((200, 200), Image.ANTIALIAS)
        self.photo_image = ImageTk.PhotoImage(img)
        self.photo_label.configure(image=self.photo_image)
        self.photo_label.image = self.photo_image  # Mantener la referencia de la imagen

    def registrar(self):
        alumno_data = (
            self.entries["Código"].get(),
            self.entries["Nombre"].get(),
            self.entries["Apellido"].get(),
            self.entries["Email"].get(),
            self.entries["Teléfono"].get(),
            self.entries["Ciclo"].get(),
        )
        try:
            self.db_manager.insert_alumno(alumno_data)
            messagebox.showinfo(
                title="Información", message="Alumno registrado con éxito"
            )
            self.load_data()
        except Exception as e:
            messagebox.showerror(title="Error", message=str(e))

    def actualizar(self):
        selected_items = self.treeview.selection()
        if not selected_items:
            messagebox.showinfo("Selección", "No se ha seleccionado ningún elemento.")
            return

        selected_item = selected_items[0]
        alumno_data = (
            self.entries["Código"].get(),
            self.entries["Nombre"].get(),
            self.entries["Apellido"].get(),
            self.entries["Email"].get(),
            self.entries["Teléfono"].get(),
            self.entries["Ciclo"].get(),
            self.treeview.item(selected_item, "values")[0],  # ID del alumno
        )
        try:
            self.db_manager.update_alumno(alumno_data)
            messagebox.showinfo(
                title="Información", message="Alumno actualizado con éxito"
            )
            self.load_data()
        except Exception as e:
            messagebox.showerror(title="Error", message=str(e))

    def eliminar(self):
        selected_items = self.treeview.selection()
        if not selected_items:
            messagebox.showinfo("Selección", "No se ha seleccionado ningún elemento.")
            return

        selected_item = selected_items[0]
        alumno_id = self.treeview.item(selected_item, "values")[0]
        try:
            self.db_manager.delete_alumno(alumno_id)
            messagebox.showinfo(
                title="Información", message="Alumno eliminado con éxito"
            )
            self.load_data()
        except Exception as e:
            messagebox.showerror(title="Error", message=str(e))

    def load_data(self):
        for i in self.treeview.get_children():
            self.treeview.delete(i)
        for row in self.db_manager.fetch_all_alumnos():
            self.treeview.insert("", "end", values=row)

    def on_treeview_click(self, event):
        selected_items = self.treeview.selection()
        if not selected_items:
            return

        selected_item = selected_items[0]
        item_values = self.treeview.item(selected_item, "values")
        for index, key in enumerate(
            ["Código", "Nombre", "Apellido", "Email", "Teléfono", "Ciclo"]
        ):
            self.entries[key].delete(0, "end")
            self.entries[key].insert(0, item_values[index + 1])


if __name__ == "__main__":
    db_manager = DatabaseManager(
        host="localhost", user="root", password="123456789", database="tutoria"
    )
    app = AlumnoApp(db_manager)
    app.root.mainloop()
