import pandas as pd
import unicodedata
import requests
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io

# Cargo el Excel
url = "https://docs.google.com/spreadsheets/d/1b8KX6KovY80b3yszO4QvFf-kJzgcD5uquhLQZFAOnd8/export?format=xlsx"
df = pd.read_excel(url)

def PCRandom(df):
    randI = random.randint(0, len(df)-1)  # número aleatorio dentro del rango
    pais = df.iloc[randI, 0]              # columna 1 = país
    capital = df.iloc[randI, 2]           # columna 3 = capital
    bandera = df.iloc[randI, 5] if df.shape[1] > 5 else None  # columna 6 = link bandera
    return (pais, capital, bandera)

def quitar_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', str(texto))
        if unicodedata.category(c) != 'Mn'
    )

def cargar_bandera(url):
    """Descarga la imagen desde el link y la adapta para Tkinter"""
    try:
        resp = requests.get(url, timeout=5)
        img_data = resp.content
        img = Image.open(io.BytesIO(img_data))
        img = img.resize((100, 60))  # tamaño de la bandera
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print("Error cargando bandera:", e)
        return None

def nueva_pregunta():
    global quiz, opciones, bandera_img
    quiz = PCRandom(df)
    opciones = [quiz[1]]

    while len(opciones) < 4:
        randI = random.randint(0, len(df)-1)
        capital_opcion = df.iloc[randI, 2]
        if capital_opcion not in opciones:
            opciones.append(capital_opcion)

    random.shuffle(opciones)

    # Mostrar pregunta
    lbl_pregunta.config(text=f"¿Cuál es la capital de {quiz[0]}?")

    # Mostrar bandera si hay link
    if quiz[2]:
        bandera_img = cargar_bandera(quiz[2])
        if bandera_img:
            lbl_bandera.config(image=bandera_img)
        else:
            lbl_bandera.config(image="", text="(Sin bandera)")
    else:
        lbl_bandera.config(image="", text="")

    # Habilitar botones
    for i, opcion in enumerate(opciones):
        botones[i].config(text=opcion, state="normal")

def chequear_respuesta(i):
    elegido = opciones[i]
    if quitar_acentos(elegido.lower()) == quitar_acentos(str(quiz[1]).lower()):
        messagebox.showinfo("Resultado", "¡Bien chango!")
    else:
        messagebox.showerror("Resultado", f"Mal ahí gato. Era: {quiz[1]}")
    for b in botones:
        b.config(state="disabled")

# Función extra: mostrar datos de fila específica
def mostrar_fila(fila_num):
    if fila_num < 0 or fila_num >= len(df):
        print("Número de fila fuera de rango")
        return

    pais = df.iloc[fila_num, 0]
    capital = df.iloc[fila_num, 2]
    bandera = df.iloc[fila_num, 5] if df.shape[1] > 5 else "Sin bandera"
    posicion = df.iloc[fila_num, 6] if df.shape[1] > 6 else "Sin posición"

    print(f"País: {pais}")
    print(f"Capital: {capital}")
    print(f"Link Bandera PNG: {bandera}")
    print(f"Link Posición Geográfica: {posicion}")

# --- GUI ---
ventana = tk.Tk()
ventana.title("Quiz País - Capital")
ventana.geometry("500x300")

frame_superior = tk.Frame(ventana)
frame_superior.pack(pady=10)

lbl_pregunta = tk.Label(frame_superior, text="Pregunta", font=("Arial", 14))
lbl_pregunta.pack(side="left", padx=10)

lbl_bandera = tk.Label(frame_superior)
lbl_bandera.pack(side="right", padx=10)

botones = []
for i in range(4):
    b = tk.Button(ventana, text="", font=("Arial", 12), width=30,
                  command=lambda i=i: chequear_respuesta(i))
    b.pack(pady=5)
    botones.append(b)

btn_siguiente = tk.Button(ventana, text="Nueva pregunta", command=nueva_pregunta)
btn_siguiente.pack(pady=20)

bandera_img = None
nueva_pregunta()
mostrar_fila(0)
ventana.mainloop()

