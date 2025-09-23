import tkinter as tk
from tkinter import messagebox
import pandas as pd
import random
import unicodedata
import logging
from matplotlib import pyplot as plt
from threading import Thread
import time

# ================== CONFIGURACIÓN DE LOGGING ==================
logging.basicConfig(
    filename="quiz_log.csv",
    level=logging.INFO,
    format="%(asctime)s,%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# ================== CLASE PRINCIPAL DE LA APLICACIÓN ==================
class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz de Países y Capitales 🌎")
        self.geometry("400x300")
        self.configure(bg="#f0f0f0")
        self.resizable(False, False)

        try:
            self.df = self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error de Carga", f"No se pudo cargar la base de datos: {e}")
            self.df = None

        self.create_widgets()
    
    def cargar_datos(self):
        """Carga los datos de países y capitales desde Google Sheets."""
        url = "https://docs.google.com/spreadsheets/d/1b8KX6KovY80b3yszO4QvFf-kJzgcD5uquhLQZFAOnd8/export?format=xlsx"
        df = pd.read_excel(url)
        df = df.rename(columns={df.columns[0]: "País", df.columns[2]: "Capital"})
        return df

    def create_widgets(self):
        """Crea la interfaz principal con los botones de inicio."""
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(expand=True)

        lbl_titulo = tk.Label(main_frame,
                              text="Bienvenido al Quiz de Países 🌎",
                              font=("Arial", 18, "bold"),
                              bg="#f0f0f0",
                              fg="#333333")
        lbl_titulo.pack(pady=20)

        btn_quiz = tk.Button(main_frame,
                             text="👉 Empezar Quiz",
                             font=("Arial", 14),
                             command=self.mostrar_quiz,
                             bg="#4CAF50",
                             fg="white",
                             relief="raised",
                             padx=10,
                             pady=5)
        btn_quiz.pack(pady=10, ipadx=20)
        
        btn_stats = tk.Button(main_frame,
                              text="📊 Ver Estadísticas",
                              font=("Arial", 14),
                              command=self.mostrar_estadisticas,
                              bg="#2196F3",
                              fg="white",
                              relief="raised",
                              padx=10,
                              pady=5)
        btn_stats.pack(pady=10, ipadx=10)

        btn_salir = tk.Button(main_frame,
                              text="🚪 Salir",
                              font=("Arial", 14),
                              command=self.quit,
                              bg="#F44336",
                              fg="white",
                              relief="raised",
                              padx=10,
                              pady=5)
        btn_salir.pack(pady=10, ipadx=35)
    
    def mostrar_quiz(self):
        """Abre la ventana del quiz."""
        if self.df is None or self.df.empty:
            messagebox.showerror("Error", "No se puede iniciar el quiz. Datos no disponibles.")
            return

        quiz_window = QuizWindow(self, self.df)
        quiz_window.grab_set()

    def mostrar_estadisticas(self):
        """Muestra las estadísticas de aciertos por país en un gráfico de barras."""
        try:
            df_log = pd.read_csv(
                "quiz_log.csv",
                names=["fecha", "pais", "capital_correcta", "respuesta", "resultado"],
                encoding='latin-1'  # <--- Agrega esta línea
            )
            
            stats = df_log.groupby("pais")["resultado"].apply(lambda x: (x=="ACIERTO").mean()*100)
            stats = stats.sort_values()

            plt.figure(figsize=(10, 6))
            stats.plot(kind="bar", color="skyblue", edgecolor="gray")
            plt.title("Porcentaje de aciertos por país", fontsize=16, weight="bold")
            plt.ylabel("Porcentaje de aciertos (%)", fontsize=12)
            plt.xlabel("País", fontsize=12)
            plt.xticks(rotation=45, ha="right")
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()

        except FileNotFoundError:
            messagebox.showerror("Error", "No hay registros aún. ¡Primero jugá un quiz!")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al generar las estadísticas: {e}")

# ================== CLASE DE LA VENTANA DEL QUIZ ==================
class QuizWindow(tk.Toplevel):
    def __init__(self, parent, df):
        super().__init__(parent)
        self.title("Quiz de Países y Capitales")
        self.geometry("600x450")
        self.configure(bg="#ffffff")
        self.resizable(False, False)
        
        self.df = df
        self.pregunta_actual = 0
        self.aciertos = 0
        self.fallos = 0
        self.quiz = None
        self.opciones = []

        self.create_widgets()
        self.nueva_pregunta()

    def create_widgets(self):
        """Crea todos los widgets de la ventana del quiz."""
        main_frame = tk.Frame(self, bg="#ffffff", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        self.lbl_pregunta_contador = tk.Label(main_frame, text="Pregunta 1", font=("Arial", 12), bg="#ffffff")
        self.lbl_pregunta_contador.pack(anchor="ne")

        self.lbl_puntuacion = tk.Label(main_frame, text="Aciertos: 0 | Fallos: 0", font=("Arial", 12), bg="#ffffff")
        self.lbl_puntuacion.pack(anchor="ne", pady=(0, 10))

        self.lbl_pais = tk.Label(main_frame,
                                 text="Cargando pregunta...",
                                 font=("Arial", 22, "bold"),
                                 fg="#005a9c",
                                 bg="#ffffff",
                                 wraplength=550)
        self.lbl_pais.pack(pady=30, fill="x")

        self.opciones_frame = tk.Frame(main_frame, bg="#ffffff")
        self.opciones_frame.pack(pady=20)
        
        self.botones = []
        for i in range(4):
            b = tk.Button(self.opciones_frame,
                          text="",
                          font=("Arial", 14),
                          width=30,
                          bg="#e0e0e0",
                          relief="raised",
                          command=lambda i=i: Thread(target=self.chequear_respuesta_thread, args=(i,)).start())
            b.grid(row=i // 2, column=i % 2, padx=10, pady=10)
            self.botones.append(b)

    def quitar_acentos(self, texto):
        """Elimina los acentos de una cadena de texto."""
        return ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )
    
    def nueva_pregunta(self):
        """Configura una nueva pregunta del quiz."""
        self.pregunta_actual += 1
        self.lbl_pregunta_contador.config(text=f"Pregunta {self.pregunta_actual}")
        
        fila = self.df.sample(1).iloc[0]
        pais = fila["País"]
        capital_correcta = fila["Capital"]

        opciones_incorrectas = self.df[self.df["Capital"] != capital_correcta].sample(3)["Capital"].tolist()
        self.opciones = [capital_correcta] + opciones_incorrectas
        random.shuffle(self.opciones)

        self.quiz = (pais, capital_correcta)

        self.lbl_pais.config(text=f"¿Cuál es la capital de {pais}?")
        for i, b in enumerate(self.botones):
            b.config(text=self.opciones[i], state="normal", bg="#e0e0e0")

    def chequear_respuesta_thread(self, i):
        """Llama a la función de chequeo de respuesta en un hilo separado para no bloquear la UI."""
        self.chequear_respuesta(i)

    def chequear_respuesta(self, i):
        """Verifica la respuesta del usuario, actualiza la interfaz y el log."""
        elegido = self.opciones[i]
        correcto = self.quitar_acentos(str(self.quiz[1]).lower())
        respuesta = self.quitar_acentos(elegido.lower())
        
        # Deshabilitar todos los botones para evitar múltiples clics
        for b in self.botones:
            b.config(state="disabled")

        es_correcto = (respuesta == correcto)
        
        # Encontrar el botón de la respuesta correcta
        correct_button_index = self.opciones.index(self.quiz[1])
        
        if es_correcto:
            self.aciertos += 1
            self.botones[i].config(bg="#A5D6A7") # Verde
            logging.info(f"{self.quiz[0]},{self.quiz[1]},{elegido},ACIERTO")
        else:
            self.fallos += 1
            self.botones[i].config(bg="#EF9A9A") # Rojo
            self.botones[correct_button_index].config(bg="#A5D6A7") # Resaltar la correcta en verde
            logging.info(f"{self.quiz[0]},{self.quiz[1]},{elegido},FALLO")

        self.lbl_puntuacion.config(text=f"Aciertos: {self.aciertos} | Fallos: {self.fallos}")

        # Esperar 1.5 segundos antes de la siguiente pregunta
        self.after(1500, self.nueva_pregunta)

# ================== PUNTO DE ENTRADA ==================
if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()