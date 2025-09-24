import requests
from PIL import Image
from io import BytesIO

# URL de la imagen
url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Europe-Albania.svg/1024px-Europe-Albania.svg.png"

# Diccionario de encabezados para simular una solicitud de navegador
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

try:
    # Descargar el contenido de la imagen usando los headers
    response = requests.get(url, headers=headers)
    
    # Verificar que la solicitud fue exitosa
    if response.status_code == 200:
        # Abrir la imagen desde la memoria (BytesIO)
        imagen = Image.open(BytesIO(response.content))
        
        # Mostrar la imagen
        imagen.show()
        
        # Opcional: guardar la imagen localmente
        # imagen.save("bandera_argentina.png")
        
        print("Imagen abierta y mostrada correctamente.")
    else:
        print(f"Error al descargar la imagen. Código de estado: {response.status_code}")
        
except requests.exceptions.RequestException as e:
    print(f"Error de conexión: {e}")
except Exception as e:
    print(f"Ocurrió un error: {e}")