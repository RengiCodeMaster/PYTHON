import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector


# Función para mostrar los datos en el Treeview
def mostrar():
    # Limpiar Treeview
    for row in tvProfesores.get_children():
        tvProfesores.delete(row)

    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="123456789",
            database="hello_mysql",
        )
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM hello_mysql.profesores")

        for row in cursor:
            tvProfesores.insert("", "end", id_profesor, text=id_profesor, values=row)

        cursor.close()
        conexion.close()

    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Error al obtener datos: {error}")


# Función para insertar un nuevo registro
def insertar():
    # Obtener los valores de los campos de entrada
    codigo = Codigo.get()
    nombre = Nombre.get()
    apellido = Apellido.get()
    email = Email.get()
    genero = Genero.get()
    horario = Horario.get()

    try:
        conexion = mysql.connector.connect(
            host="localhost", user="root", passwd="123456789", database="hello_mysql"
        )
        cursor = conexion.cursor()
        sql = "INSERT INTO profesores (codigo, nombre, apellido, email, genero, horario) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = (codigo, nombre, apellido, email, genero, horario)
        cursor.execute(sql, valores)
        conexion.commit()
        messagebox.showinfo("Éxito", "Registro insertado correctamente")
        limpiar_campos()
        mostrar()

    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Error al insertar el registro: {error}")

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()


# Función para limpiar los campos de entrada
def limpiar_campos():
    Codigo.set("")
    Nombre.set("")
    Apellido.set("")
    Email.set("")
    Genero.set("")
    Horario.set("")


# Función para eliminar un registro seleccionado
def eliminar():
    seleccionado = tvProfesores.selection()
    if not seleccionado:
        messagebox.showwarning(
            "Eliminar", "Por favor, selecciona un registro para eliminar."
        )
        return

    confirmar = messagebox.askyesno(
        "Eliminar", "¿Estás seguro que deseas eliminar este registro?"
    )
    if confirmar:
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="123456789",
                database="hello_mysql",
            )
            cursor = conexion.cursor()
            codigo = tvProfesores.item(seleccionado, "values")[
                0
            ]  # Suponiendo que el código es el primer valor
            sql = "DELETE FROM Profesores WHERE codigo = %s"
            cursor.execute(sql, (codigo))
            conexion.commit()
            messagebox.showinfo("Éxito", "Registro eliminado correctamente")
            mostrar()

        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Error al eliminar el registro: {error}")

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()


# Crear la ventana principal
app = tk.Tk()
app.title("Tutorias")
app.geometry("600x500")

# Variables para interactuar con la base de datos
id_profesor = tk.IntVar()
Codigo = tk.StringVar()
Nombre = tk.StringVar()
Apellido = tk.StringVar()
Email = tk.StringVar()
Genero = tk.StringVar()
Horario = tk.StringVar()

# Crear el marco para la interfaz
marco = tk.LabelFrame(app, text="Seleccion de tutoria", bg="lightblue")
marco.place(x=10, y=10, width=600, height=500)

# Etiquetas y entradas para los datos del estudiante
tk.Label(marco, text="Codigo").grid(column=0, row=0, padx=5, pady=5)
tk.Entry(marco, textvariable=Codigo).grid(column=1, row=0, padx=5, pady=5)

tk.Label(marco, text="Nombre").grid(column=0, row=1, padx=5, pady=5)
tk.Entry(marco, textvariable=Nombre).grid(column=1, row=1, padx=5, pady=5)

tk.Label(marco, text="Apellido").grid(column=0, row=2, padx=5, pady=5)
tk.Entry(marco, textvariable=Apellido).grid(column=1, row=2, padx=5, pady=5)

tk.Label(marco, text="Email").grid(column=2, row=0, padx=5, pady=5)
tk.Entry(marco, textvariable=Email).grid(column=3, row=0, padx=5, pady=5)

tk.Label(marco, text="Genero").grid(column=2, row=1, padx=5, pady=5)
tk.Entry(marco, textvariable=Genero).grid(column=3, row=1, padx=5, pady=5)

tk.Label(marco, text="Horario").grid(column=2, row=2, padx=5, pady=5)
tk.Entry(marco, textvariable=Horario).grid(column=3, row=2, padx=5, pady=5)

# Botones para operaciones CRUD
btnMostrar = tk.Button(marco, text="Mostrar", command=mostrar)
btnMostrar.grid(column=0, row=4, padx=10, pady=10)

btnInsertar = tk.Button(marco, text="Insertar", command=insertar)
btnInsertar.grid(column=1, row=4, padx=10, pady=10)

btnEliminar = tk.Button(marco, text="Eliminar", command=eliminar)
btnEliminar.grid(column=2, row=4, padx=10, pady=10)

# Treeview para mostrar los datos
tvProfesores = ttk.Treeview(
    marco, columns=("Codigo", "Nombre", "Apellido", "Email", "Genero", "Horario")
)
tvProfesores.grid(column=0, row=5, columnspan=5, padx=10, pady=10)

tvProfesores["show"] = "headings"
tvProfesores.column("#0", width=0, stretch=tk.NO)
tvProfesores.column("Codigo", width=50, anchor="center")
tvProfesores.column("Nombre", width=100, anchor="center")
tvProfesores.column("Apellido", width=100, anchor="center")
tvProfesores.column("Email", width=150, anchor="center")
tvProfesores.column("Genero", width=100, anchor="center")
tvProfesores.column("Horario", width=100, anchor="center")

tvProfesores.heading("#0", text="")
tvProfesores.heading("Codigo", text="Codigo")
tvProfesores.heading("Nombre", text="Nombre")
tvProfesores.heading("Apellido", text="Apellido")
tvProfesores.heading("Email", text="Email")
tvProfesores.heading("Genero", text="Genero")
tvProfesores.heading("Horario", text="Horario")

app.mainloop()
