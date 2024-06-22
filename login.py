from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from main import ProfesoresApp


class LoginApp:
    def __init__(self):
        self.app = Tk()
        self.app.title("Login")
        self.app.geometry("300x200")

        self.username = StringVar()
        self.password = StringVar()
        self.role = StringVar()

        self.create_widgets()
        self.app.mainloop()

    def create_widgets(self):
        Label(self.app, text="Username").grid(column=0, row=0, padx=5, pady=5)
        Entry(self.app, textvariable=self.username).grid(
            column=1, row=0, padx=5, pady=5
        )

        Label(self.app, text="Password").grid(column=0, row=1, padx=5, pady=5)
        Entry(self.app, textvariable=self.password, show="*").grid(
            column=1, row=1, padx=5, pady=5
        )

        Label(self.app, text="Role").grid(column=0, row=2, padx=5, pady=5)

        # Combobox for role selection
        self.combobox_role = ttk.Combobox(
            self.app, textvariable=self.role, state="readonly"
        )
        self.combobox_role["values"] = ("Estudiante", "Profesor")
        self.combobox_role.grid(column=1, row=2, padx=5, pady=5)

        Button(self.app, text="Login", command=self.login).grid(
            column=1, row=3, padx=5, pady=5
        )

    def login(self):
        username = self.username.get()
        password = self.password.get()
        role = self.role.get()

        if not username or not password or not role:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        else:
            messagebox.showinfo("Login", f"Login exitoso como {role}")
            if role == "Profesor":

                self.app.destroy()
                ProfesoresApp()
            elif role == "Estudiante":
                pass


if __name__ == "__main__":
    app = LoginApp()
