import requests
from bs4 import BeautifulSoup
import datetime
import csv
import os

def scraper_basico():
    url = "http://books.toscrape.com/"
    print(f"🔍 Conectando a {url}...")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraer primer libro como prueba
        producto = soup.find('article', class_='product_pod')
        titulo = producto.h3.a['title']
        precio = producto.find('p', class_='price_color').text
        
        # Guardar en CSV
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        archivo = 'resultados.csv'
        existe = os.path.isfile(archivo)
        
        with open(archivo, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not existe:
                writer.writerow(['Fecha', 'Titulo', 'Precio'])
            writer.writerow([fecha, titulo, precio])
        
        print(f"✅ {titulo} - {precio}")
        print(f"💾 Guardado en {archivo}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

if __name__ == "__main__":
    scraper_basico()
