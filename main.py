from tkinter import *
from tkinter import ttk


# Crea la ventana
def prosefores():
    app = Tk()

    app.title("Tutorias")
    app.geometry("600x300")

    # Declaramos las variables para interactuar con la base de datos

    Codigo = StringVar()
    Nombre = StringVar()
    Apellido = StringVar()
    Email = StringVar()
    Genero = StringVar()
    Horario = StringVar()

    # Crea el marco en la parte superior
    marco = LabelFrame(app, text="Seleccion de tutoria", bg="lightblue")
    marco.place(x=10, y=10, width=580, height=250)

    # Crea los elementos del marco
    lbCodigo = Label(marco, text="Codigo").grid(column=0, row=0, padx=5, pady=5)
    txtCodigo = Entry(marco, textvariable=Codigo)
    txtCodigo.grid(column=1, row=0, padx=5, pady=5)

    lbNombre = Label(marco, text="Nombre").grid(column=0, row=1, padx=5, pady=5)
    txtNombre = Entry(marco, textvariable=Nombre)
    txtNombre.grid(column=1, row=1, padx=5, pady=5)

    lbApellido = Label(marco, text="Apellido").grid(column=0, row=2, padx=5, pady=5)
    txtApellido = Entry(marco, textvariable=Apellido)
    txtApellido.grid(column=1, row=2, padx=5, pady=5)

    lbEmail = Label(marco, text="Email").grid(column=2, row=0, padx=5, pady=5)
    txtEmail = Entry(marco, textvariable=Email)
    txtEmail.grid(column=3, row=0, padx=5, pady=5)

    lbGenero = Label(marco, text="Genero").grid(column=2, row=1, padx=5, pady=5)
    txtGenero = Entry(marco, textvariable=Genero)
    txtGenero.grid(column=3, row=1, padx=5, pady=5)

    lbHorario = Label(marco, text="Horario").grid(column=2, row=2, padx=5, pady=5)
    txtHorario = Entry(marco, textvariable=Horario)
    txtHorario.grid(column=3, row=2, padx=5, pady=5)

    app.mainloop()


if __name__ == "__main__":
    prosefores()
