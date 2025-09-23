import tkinter as tk
from tkinter import messagebox
import pandas as pd
import random
import unicodedata
import logging
from matplotlib import pyplot as plt

# ================== CONFIGURACIÓN DE LOGGING ==================
logging.basicConfig(
    filename="quiz_log.csv",
    level=logging.INFO,
    format="%(asctime)s,%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# ================== FUNCIONES AUXILIARES ==================
def quitar_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def cargar_datos():
    url = "https://docs.google.com/spreadsheets/d/1b8KX6KovY80b3yszO4QvFf-kJzgcD5uquhLQZFAOnd8/export?format=xlsx"
    df = pd.read_excel(url)
    df = df.rename(columns={df.columns[0]: "País", df.columns[2]: "Capital"})
    return df


def nueva_pregunta():
    global quiz, opciones

    fila = df.sample(1).iloc[0]
    pais = fila["País"]
    capital_correcta = fila["Capital"]

    opciones = [capital_correcta] + list(df.sample(3)["Capital"])
    random.shuffle(opciones)

    quiz = (pais, capital_correcta)

    lbl_pais.config(text=f"¿Cuál es la capital de {pais}?")
    for i, b in enumerate(botones):
        b.config(text=opciones[i], state="normal")

def chequear_respuesta(i):
    elegido = opciones[i]
    correcto = quitar_acentos(str(quiz[1]).lower())
    respuesta = quitar_acentos(elegido.lower())

    if respuesta == correcto:
        messagebox.showinfo("Resultado", "¡Bien chango! ✅")
        logging.info(f"{quiz[0]},{quiz[1]},{elegido},ACIERTO")
    else:
        messagebox.showerror("Resultado", f"Mal ahí gato ❌. Era: {quiz[1]}")
        logging.info(f"{quiz[0]},{quiz[1]},{elegido},FALLO")

    for b in botones:
        b.config(state="disabled")

def mostrar_quiz():
    global quiz, opciones, lbl_pais, botones, df

    quiz_window = tk.Toplevel(ventana)
    quiz_window.title("Quiz de Países y Capitales")
    quiz_window.geometry("400x300")

    lbl_pais = tk.Label(quiz_window, text="", font=("Arial", 14))
    lbl_pais.pack(pady=20)

    botones = []
    for i in range(4):
        b = tk.Button(quiz_window, text="", font=("Arial", 12),
                      command=lambda i=i: chequear_respuesta(i))
        b.pack(pady=5)
        botones.append(b)

    btn_siguiente = tk.Button(quiz_window, text="Siguiente", command=nueva_pregunta)
    btn_siguiente.pack(pady=20)

    nueva_pregunta()

def mostrar_estadisticas():
    try:
        df_log = pd.read_csv(
            "quiz_log.csv",
            names=["fecha","pais","capital_correcta","respuesta","resultado"]
        )

        # porcentaje de aciertos por país
        stats = df_log.groupby("pais")["resultado"].apply(lambda x: (x=="ACIERTO").mean()*100)

        # ordenar de peor a mejor
        stats = stats.sort_values()

        plt.figure(figsize=(8,5))
        stats.plot(kind="bar", color="skyblue")
        plt.title("Porcentaje de aciertos por país")
        plt.ylabel("% de aciertos")
        plt.xlabel("País")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        messagebox.showerror("Error", "No hay registros aún. ¡Primero jugá un quiz!")

# ================== VENTANA PRINCIPAL ==================
df = cargar_datos()

ventana = tk.Tk()
ventana.title("Quiz de Países")
ventana.geometry("300x200")

lbl = tk.Label(ventana, text="Bienvenido al Quiz de Países 🌎", font=("Arial", 12))
lbl.pack(pady=20)

btn_quiz = tk.Button(ventana, text="👉 Empezar Quiz", font=("Arial", 12), command=mostrar_quiz)
btn_quiz.pack(pady=10)

btn_stats = tk.Button(ventana, text="📊 Ver Estadísticas", font=("Arial", 12), command=mostrar_estadisticas)
btn_stats.pack(pady=10)

ventana.mainloop()
