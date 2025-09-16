import pandas as pd
import unicodedata
import requests
import random
from PIL import Image
from io import BytesIO

#cargo el excel
url = "https://docs.google.com/spreadsheets/d/1f3FDyCojxebsl3EL6n2dyEq-SxAYPBsAlRAgq7oSiBQ/export?format=xlsx"
df = pd.read_excel(url)

# Mostrar primeras filas para ver la estructura
#print(df.head())

def PCAmericaSur (df):
    randI= random.randint (0,11)
    pais = df.iloc[randI, 0] # primera columna = país
    capital = df.iloc[randI, 1] # segunda columna = capital
    return (pais, capital)

def quitar_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', str(texto))
        if unicodedata.category(c) != 'Mn'
    )

def quizPaisCapitalAmericaSur(df):
    quiz = PCAmericaSur(df)  # devuelve (pais, capital)
    print("¿Cuál es la capital de:", quiz[0], "?")
    intento = input("Decime la capital: ")

    # Pasar a minúsculas y quitar acentos
    intento_norm = quitar_acentos(intento.strip().lower())
    capital_norm = quitar_acentos(str(quiz[1]).lower())

    if intento_norm == capital_norm:
        print("¡Bien chango!")
    else:
        print("Mal ahí gato. La respuesta correcta es:", quiz[1])


quizPaisCapitalAmericaSur(df)