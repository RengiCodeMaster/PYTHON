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

        self.username = StringVar()
        self.password = StringVar()
        self.role = StringVar()
        self.create_widgets()
        self.app.mainloop()

    def create_widgets(self):
        # Create a responsive frame
        marco = LabelFrame(
            self.app,
            text="LOGIN",
            bg="#FFFFFF",
            font=("Arial", 16, "bold"),
            # image_namespace="login.png",
        )
        marco.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(0, weight=1)

        # Add labels and entry widgets
        Label(marco, text="Username:", bg="#FFFFFF", font=("Arial", 12)).grid(
            column=0, row=0, padx=10, pady=10, sticky=E
        )
        Entry(marco, textvariable=self.username, font=("Arial", 12)).grid(
            column=1, row=0, padx=10, pady=10, sticky=W
        )

        Label(marco, text="Password:", bg="#FFFFFF", font=("Arial", 12)).grid(
            column=0, row=1, padx=10, pady=10, sticky=E
        )
        Entry(marco, textvariable=self.password, show="*", font=("Arial", 12)).grid(
            column=1, row=1, padx=10, pady=10, sticky=W
        )

        Label(marco, text="Role:", bg="#FFFFFF", font=("Arial", 12)).grid(
            column=0, row=2, padx=10, pady=10, sticky=E
        )

        self.combobox_role = ttk.Combobox(
            marco, textvariable=self.role, state="readonly", font=("Arial", 12)
        )
        self.combobox_role["values"] = ("Estudiante", "Profesor")
        self.combobox_role.grid(column=1, row=2, padx=10, pady=10, sticky=W)

        Button(
            marco,
            text="Login",
            command=self.login,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12),
        ).grid(column=1, row=3, padx=10, pady=20, sticky=W)

        # Configure grid weights to make it responsive
        for i in range(2):
            marco.grid_columnconfigure(i, weight=1)
        for i in range(4):
            marco.grid_rowconfigure(i, weight=1)

    def login(self):
        username = self.username.get()
        password = self.password.get()
        role = self.role.get()

        # Input validation with feedback
        if not username or not password or not role:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        elif len(username) < 3 or len(password) < 5:
            messagebox.showerror(
                "Error",
                "Username debe tener al menos 3 caracteres y Password al menos 5 caracteres",
            )
            return
        else:
            messagebox.showinfo("Login", f"Login exitoso como {role}")
            if role == "Profesor":
                self.app.destroy()
                ProfesoresApp()
            elif role == "Estudiante":
                self.app.destroy()
                AlumnoApp()


if __name__ == "__main__":
    app = LoginApp()
