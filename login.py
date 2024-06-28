from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from profesores import ProfesoresApp
from alumnos import AlumnoApp


class LoginApp:
    def __init__(self):
        self.app = Tk()
        self.app.title("Login")
        self.app.geometry("500x400")
        self.app.configure(bg="#F0F0F0")
        self.role = StringVar()
        self.create_widgets()
        self.app.mainloop()

    def create_widgets(self):
        # Create a responsive frame
        marco = LabelFrame(
            self.app,
            text="LOGIN",
            bg="#16F58B",
            font=("Arial", 16, "bold"),
        )
        marco.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.porfile_img1 = PhotoImage(file="./example/icons8-add-user-male-48.png")

        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(0, weight=1)

        Button(
            marco,
            text="Role:",
            bg="#FFFFFF",
            font=("Arial", 12),
            image=self.porfile_img1,
            command=self.select_role,
        ).grid(column=1, row=1, padx=10, pady=10, sticky=W)

        Button(
            marco,
            text="Login",
            command=self.login,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12),
        ).grid(column=1, row=3, padx=10, pady=20, sticky=W)

        for i in range(2):
            marco.grid_columnconfigure(i, weight=1)
        for i in range(4):
            marco.grid_rowconfigure(i, weight=1)

    def select_role(self):

        pass

    def login(self):
        role = self.role.get()
        if role == "Profesor":
            messagebox.showinfo("Login", "Login exitoso como Profesor")
            self.app.destroy()
            ProfesoresApp()

        elif role == "Estudiante":
            messagebox.showinfo("Login", "Login exitoso como Estudiante")
            self.app.destroy()
            AlumnoApp()


if __name__ == "__main__":
    app = LoginApp()
