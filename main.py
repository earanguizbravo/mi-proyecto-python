import requests
from bs4 import BeautifulSoup
import datetime
import csv
import os

def obtener_precio_libro():
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Datos a guardar
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    producto = soup.find('article', class_='product_pod')
    titulo = producto.h3.a['title']
    precio = producto.find('p', class_='price_color').text
    
    # Guardar en CSV
    archivo = 'resultados.csv'
    existe = os.path.isfile(archivo)
    
    with open(archivo, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow(['Fecha', 'Titulo', 'Precio']) # Cabecera
        writer.writerow([fecha, titulo, precio])
    
    print(f"✅ Datos guardados en {archivo}")

if __name__ == "__main__":
    obtener_precio_libro()
