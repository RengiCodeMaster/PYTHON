from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class AlumnoApp:
    def __init__(self):
        self.app = Tk()
        self.app.title("Alumno")
        self.app.geometry("500x400")

        self.username = StringVar()
        self.password = StringVar()
        self.role = StringVar()

        self.create_widgets()
        self.app.mainloop()

    def create_widgets(self):
        marco = LabelFrame(self.app, text="ALUMNO", bg="#F5F5DC")
        marco.place(x=15, y=15, width=750, height=500)

        self.app_grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(0, weight=1)


if __name__ == "__main__":
    AlumnoApp()
