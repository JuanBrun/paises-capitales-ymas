import pandas as pd
import unicodedata
import requests
import random

#cargo el excel
url = "https://docs.google.com/spreadsheets/d/1b8KX6KovY80b3yszO4QvFf-kJzgcD5uquhLQZFAOnd8/export?format=xlsx"

df = pd.read_excel(url)

# Mostrar primeras filas para ver la estructura
#print(df.head())

def PCRandom (df):
    randI= random.randint (0,196) #elige un número al azar entre 0 y 196
    pais = df.iloc[randI, 0] # primera columna = país
    capital = df.iloc[randI, 2] # tercera columna = capital
    return (pais, capital)

def quitar_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', str(texto))
        if unicodedata.category(c) != 'Mn'
    )

def quizPaisCapital(quiz):
    print("¿Cuál es la capital de:", quiz[0], "?")
    intento = input("Decime la capital: ")

    # Pasar a minúsculas y quitar acentos
    intento_norm = quitar_acentos(intento.strip().lower())
    capital_norm = quitar_acentos(str(quiz[1]).lower())

    if intento_norm == capital_norm:
        print("¡Bien chango!")
    else:
        print("Mal ahí gato. La respuesta correcta es:", quiz[1])


def quizCapitalConOpciones (quiz):
    opciones = [quiz[1]]  # Incluir la respuesta correcta
    while len(opciones) < 4:
        randI = random.randint(0, 196)
        capital_opcion = df.iloc[randI, 2]
        if capital_opcion not in opciones:
            opciones.append(capital_opcion)
    random.shuffle(opciones)

    print("¿Cuál es la capital de:", quiz[0], "?")
    for i, opcion in enumerate(opciones, 1):
        print(f"{i}. {opcion}")

    intento = input("Decime el número de la capital: ")

    try:
        intento_index = int(intento) - 1
        if opciones[intento_index] == quiz[1]:
            print("¡Bien chango!")
        else:
            print("Mal ahí gato. La respuesta correcta es:", quiz[1])
    except (ValueError, IndexError):
        print("Entrada inválida. La respuesta correcta es:", quiz[1])


while input("otro? (s/n): ").lower() == 's':
    quizCapitalConOpciones(PCRandom(df))
#prueba