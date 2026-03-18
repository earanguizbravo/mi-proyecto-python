import requests
from bs4 import BeautifulSoup
import datetime
import csv
import os

def obtener_precio_libro():
    url = "http://books.toscrape.com/"
    print(f"🔍 Conectando a {url}...")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraer todos los libros de la página
        productos = soup.find_all('article', class_='product_pod')
        
        archivo = 'resultados.csv'
        existe = os.path.isfile(archivo)
        
        with open(archivo, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Escribir cabecera si es la primera vez
            if not existe:
                writer.writerow(['Fecha', 'Titulo', 'Precio', 'Disponibilidad'])
            
            # Guardar cada libro encontrado
            for producto in productos:
                fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                titulo = producto.h3.a['title']
                precio = producto.find('p', class_='price_color').text
                disponibilidad = producto.find('p', class_='instock availability').text.strip()
                
                writer.writerow([fecha, titulo, precio, disponibilidad])
                print(f"✅ {titulo} - {precio}")
        
        print(f"\n📊 Total de libros procesados: {len(productos)}")
        print(f"💾 Datos guardados en {archivo}")
        
    except Exception as e:
        print(f"❌ Error en el scraping: {str(e)}")
        raise  # Esto hace que el workflow falle si hay error

if __name__ == "__main__":
    obtener_precio_libro()
