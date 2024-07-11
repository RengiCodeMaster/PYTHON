import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Crear una carpeta para guardar las imágenes de entrenamiento
training_data_dir = "training_data"
if not os.path.exists(training_data_dir):
    os.makedirs(training_data_dir)


# Capturar imágenes de los estudiantes
def capture_images(student_id):
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for x, y, w, h in faces:
            count += 1
            face = gray[y : y + h, x : x + w]
            face = cv2.resize(face, (200, 200))
            file_name_path = os.path.join(
                training_data_dir, f"{student_id}_{count}.jpg"
            )
            cv2.imwrite(file_name_path, face)
            cv2.putText(
                frame,
                f"Image {count}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 0, 0),
                2,
            )
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow("Capturando imagen", frame)

        if cv2.waitKey(1) & 0xFF == ord("q") or count >= 50:
            break

    cap.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Info", f"Captura {count} imagen de estudiante {student_id}")


# Entrenar el reconocedor facial
def train_model():
    faces = []
    labels = []
    label_dict = {}
    current_id = 0

    for root, dirs, files in os.walk(training_data_dir):
        for file in files:
            if file.endswith("jpg"):
                path = os.path.join(root, file)
                label = int(file.split("_")[0])
                if label not in label_dict:
                    label_dict[label] = current_id
                    current_id += 1
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                faces.append(img)
                labels.append(label_dict[label])

    faces = np.array(faces)
    labels = np.array(labels)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, labels)
    recognizer.save("face_recognizer.yml")
    np.save("label_dict.npy", label_dict)
    messagebox.showinfo("Info", "Modelo guardo correctamente")


# Reconocer al estudiante
def recognize_student():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("face_recognizer.yml")
    label_dict = np.load("label_dict.npy", allow_pickle=True).item()

    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for x, y, w, h in faces:
            face = gray[y : y + h, x : x + w]
            face = cv2.resize(face, (200, 200))
            label_id, confidence = recognizer.predict(face)
            student_id = None
            for key, value in label_dict.items():
                if value == label_id:
                    student_id = key
                    break

            cv2.putText(
                frame,
                f"ID: {student_id}, Conf: {confidence:.2f}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 0, 0),
                2,
            )
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow("Recognizing Student", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# Crear la interfaz gráfica
def create_gui():
    root = tk.Tk()
    root.title("Face Recognition Training")
    root.geometry("400x300")
    root.resizable(False, False)
    root.configure(bg="#f0f0f0")

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)
    style.configure("TLabel", font=("Helvetica", 14))

    frame = ttk.Frame(root, padding=20)
    frame.pack(expand=True)

    label = ttk.Label(frame, text="Face Recognition Training System")
    label.pack(pady=10)

    def capture_button_clicked():
        student_id = simpledialog.askstring("Input", "Enter Student ID:")
        if student_id:
            capture_images(student_id)

    def train_button_clicked():
        train_model()

    def recognize_button_clicked():
        recognize_student()

    capture_button = ttk.Button(
        frame, text="Capture Images", command=capture_button_clicked
    )
    capture_button.pack(pady=10)

    train_button = ttk.Button(frame, text="Train Model", command=train_button_clicked)
    train_button.pack(pady=10)

    recognize_button = ttk.Button(
        frame, text="Recognize Student", command=recognize_button_clicked
    )
    recognize_button.pack(pady=10)
    root.mainloop()


# Ejecutar la interfaz gráfica
create_gui()
