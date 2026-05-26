README DEL PROYECTO
Sistema Inteligente de Asistencia con Reconocimiento Facial

Sistema desarrollado en Python capaz de reconocer rostros en tiempo real utilizando inteligencia artificial y visión computacional para automatizar el registro de asistencia.

El sistema almacena automáticamente los registros y genera dashboards interactivos para análisis visual de datos.

Instalación

Crear entorno virtual con:
python -m venv yolov11_env

Activamos el entorno virtual:
yolov11_env\Scripts\actívate

Librerias a instalar:
pip install face_recognition
pip install opencv-python
pip install customtkinter
pip install pillow
pip install streamlit pandas plotly

Ejecución del Sistema
Reconocimiento Facial:
python interfaz.py

Dashboard:
streamlit run dashboard.py