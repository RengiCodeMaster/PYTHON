from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from profesores import ProfesoresApp
from alumnos import AlumnoApp
from dataBaseProfesores import DatabaseManagerProfesores


class LoginApp:

    def __init__(self):
        self.app = Tk()
        self.app.title("Login")
        self.app.geometry("600x600")
        self.app.configure(bg="#F8F8F8")
        self.role = StringVar()
        self.create_widgets()
        self.icon_img = PhotoImage(
            file="./example/UNAS.png"
        )  # Reemplaza con la ruta de tu ícono
        self.app.iconphoto(False, self.icon_img)
        self.db_manager = DatabaseManagerProfesores(
            host="localhost", user="root", password="123456789", database="tutoria"
        )
        self.app.mainloop()

    def create_widgets(self):
        # Main Frame
        main_frame = Frame(self.app, bg="#F8F8F8")
        main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Overlay Frame
        overlay_frame = Frame(
            main_frame, bg="#FFFFFF", bd=2, relief="groove", padx=20, pady=20
        )
        overlay_frame.pack()

        # Title
        title_label = Label(
            overlay_frame,
            text="LOGIN",
            bg="#FFFFFF",
            fg="#333333",
            font=("Helvetica", 28, "bold"),
        )
        title_label.pack(pady=(10, 20))

        # Select Role Button
        self.porfile_img1 = PhotoImage(file="./example/icons8-add-user-male-48.png")
        select_role_btn = Button(
            overlay_frame,
            text="Seleccionar Rol",
            bg="#FFFFFF",
            font=("Helvetica", 14),
            image=self.porfile_img1,
            command=self.select_role,
            compound=LEFT,
            padx=10,
            pady=5,
            relief=FLAT,
            cursor="hand2",
        )
        select_role_btn.pack(anchor=W, padx=20, pady=5)

        # Login Button
        login_btn = Button(
            overlay_frame,
            text="Login",
            command=self.login,
            compound=LEFT,
            bg="#3498DB",
            fg="white",
            font=("Helvetica", 16, "bold"),
            padx=20,
            pady=10,
            relief=FLAT,
            cursor="hand2",
        )
        login_btn.pack(pady=20)

    def select_role(self):
        role = Toplevel(self.app)
        role.title("Select Role")
        # role.PhotoImage(file="./example/UNAS.png")  # Reemplaza con la ruta de tu ícono
        role.geometry("350x300")
        role.configure(bg="#2C3E50")

        self.role.set(" ")

        role_label = Label(
            role,
            text="Seleccione su rol:",
            bg="#2C3E50",
            fg="#ECF0F1",
            font=("Helvetica", 16, "bold"),
        )
        role_label.pack(anchor=W, padx=10, pady=10)

        professor_radio = Radiobutton(
            role,
            text="Profesor",
            variable=self.role,
            value="Profesor",
            bg="#2C3E50",
            fg="#ECF0F1",
            selectcolor="#34495E",
            font=("Helvetica", 14),
        )
        professor_radio.pack(anchor=W, padx=20, pady=5)

        student_radio = Radiobutton(
            role,
            text="Estudiante",
            variable=self.role,
            value="Estudiante",
            bg="#2C3E50",
            fg="#ECF0F1",
            selectcolor="#34495E",
            font=("Helvetica", 14),
        )
        student_radio.pack(anchor=W, padx=20, pady=5)

        confirm_btn = Button(
            role,
            text="Confirmar",
            command=role.destroy,
            bg="#E74C3C",
            fg="white",
            font=("Helvetica", 14, "bold"),
            padx=20,
            pady=10,
            relief=FLAT,
            cursor="hand2",
        )
        confirm_btn.pack(pady=10)

        role.bind("<Return>", lambda event: self.login())

    def login(self):
        role = self.role.get()
        if role == "Profesor":
            messagebox.showinfo("Login", "Login exitoso como Profesor")
            self.app.destroy()
            ProfesoresApp(self.db_manager)
        elif role == "Estudiante":
            messagebox.showinfo("Login", "Login exitoso como Estudiante")
            self.app.destroy()
            AlumnoApp(self.db_manager)


if __name__ == "__main__":
    app = LoginApp()
