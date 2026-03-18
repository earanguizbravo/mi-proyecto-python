import requests
from bs4 import BeautifulSoup
import datetime

def obtener_precio_libro():
    url = "http://books.toscrape.com/"
    print(f"Conectando a {url}...")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Verifica si hubo error
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscamos el primer libro en la lista
        producto = soup.find('article', class_='product_pod')
        titulo = producto.h3.a['title']
        precio = producto.find('p', class_='price_color').text
        
        mensaje = f"✅ [{datetime.datetime.now()}] Libro: {titulo} | Precio: {precio}"
        print(mensaje)
        return mensaje
        
    except Exception as e:
        error = f"❌ Error en el scraping: {str(e)}"
        print(error)
        return error

if __name__ == "__main__":
    obtener_precio_libro()
