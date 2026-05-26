import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
import face_recognition
import os
import csv
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()

ventana.title("Sistema Inteligente de Asistencia")

ventana.geometry("1400x800")

ventana.state("zoomed")
ruta_rostros = "rostros"

rostros_conocidos = []
nombres_conocidos = []

for archivo in os.listdir(ruta_rostros):

    ruta_imagen = os.path.join(ruta_rostros, archivo)

    imagen = face_recognition.load_image_file(ruta_imagen)

    encodings = face_recognition.face_encodings(imagen)

    if len(encodings) > 0:

        rostros_conocidos.append(encodings[0])

        nombre = ''.join(
            [i for i in os.path.splitext(archivo)[0] if not i.isdigit()]
        )

        nombres_conocidos.append(nombre)

print("Rostros cargados correctamente.")

personas_detectadas = []

camara = cv2.VideoCapture(0)
top_frame = ctk.CTkFrame(
    ventana,
    height=90,
    corner_radius=0
)

top_frame.pack(fill="x")

titulo = ctk.CTkLabel(
    top_frame,
    text="SISTEMA INTELIGENTE DE ASISTENCIA",
    font=("Arial Black", 34)
)

titulo.pack(pady=20)
main_frame = ctk.CTkFrame(ventana)

main_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)
frame_camara = ctk.CTkFrame(
    main_frame,
    width=950,
    height=700
)

frame_camara.pack(
    side="left",
    padx=20,
    pady=20
)

label_camara = ctk.CTkLabel(
    frame_camara,
    text=""
)

label_camara.pack(padx=10, pady=10)
panel = ctk.CTkFrame(
    main_frame,
    width=350
)

panel.pack(
    side="right",
    fill="y",
    padx=15,
    pady=15
)

titulo_panel = ctk.CTkLabel(
    panel,
    text="PERSONAS DETECTADAS",
    font=("Arial Black", 24)
)

titulo_panel.pack(pady=20)
textbox = ctk.CTkTextbox(
    panel,
    width=300,
    height=320,
    font=("Arial", 18),
    corner_radius=12
)

textbox.pack(pady=10)
hora_label = ctk.CTkLabel(
    panel,
    text="",
    font=("Arial Black", 28)
)

hora_label.pack(pady=15)
fecha_label = ctk.CTkLabel(
    panel,
    text="",
    font=("Arial", 20)
)

fecha_label.pack(pady=5)
estado = ctk.CTkLabel(
    panel,
    text="● SISTEMA ACTIVO",
    text_color="lightgreen",
    font=("Arial Black", 20)
)

estado.pack(pady=15)
contador_label = ctk.CTkLabel(
    panel,
    text="Personas: 0",
    font=("Arial Black", 22)
)

contador_label.pack(pady=10)
def actualizar_video():

    ret, frame = camara.read()

    if ret:

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        ubicaciones = face_recognition.face_locations(rgb)

        encodings = face_recognition.face_encodings(
            rgb,
            ubicaciones
        )

        for (top, right, bottom, left), rostro_encoding in zip(
            ubicaciones,
            encodings
        ):

            coincidencias = face_recognition.compare_faces(
                rostros_conocidos,
                rostro_encoding,
                tolerance=0.45
            )

            nombre = "Desconocido"

            if True in coincidencias:

                indice = coincidencias.index(True)

                nombre = nombres_conocidos[indice]

            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                (0,255,0),
                3
            )
            cv2.putText(
                frame,
                nombre,
                (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2
            )
            if nombre != "Desconocido" and nombre not in personas_detectadas:

                personas_detectadas.append(nombre)

                fecha = datetime.now().strftime("%d/%m/%Y")

                hora = datetime.now().strftime("%H:%M:%S")

                

                ventana.bell()

                

                with open(
                    "asistencia.csv",
                    "a",
                    newline=""
                ) as archivo_csv:

                    writer = csv.writer(archivo_csv)

                    writer.writerow([
                        nombre,
                        fecha,
                        hora
                    ])


                textbox.insert(
                    "end",
                    f"{nombre}   |   {hora}\n"
                )

                textbox.see("end")

                contador_label.configure(
                    text=f"Personas: {len(personas_detectadas)}"
                )

        hora_actual = datetime.now().strftime("%H:%M:%S")

        hora_label.configure(
            text=f"Hora Actual\n{hora_actual}"
        )
        fecha_actual = datetime.now().strftime("%d/%m/%Y")

        fecha_label.configure(
            text=f"Fecha\n{fecha_actual}"
        )
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        imagen = Image.fromarray(frame)

        imagen = imagen.resize((950, 700))

        foto = ImageTk.PhotoImage(imagen)

        label_camara.configure(image=foto)

        label_camara.image = foto

    ventana.after(10, actualizar_video)


def limpiar():

    textbox.delete("1.0", "end")

def cerrar():

    camara.release()

    ventana.destroy()

boton_limpiar = ctk.CTkButton(
    panel,
    text="Limpiar Panel",
    command=limpiar,
    height=45,
    font=("Arial Black", 18)
)

boton_limpiar.pack(pady=15)

boton_salir = ctk.CTkButton(
    panel,
    text="Cerrar Sistema",
    command=cerrar,
    fg_color="red",
    hover_color="#E63A8A",
    height=50,
    font=("Arial Black", 20)
)

boton_salir.pack(pady=20)
actualizar_video()

ventana.mainloop()