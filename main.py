import requests
from bs4 import BeautifulSoup
import datetime
import csv
import os
import time

# ─────────────────────────────────────────────────────────────
# FUNCIÓN: Enviar notificación a Telegram
# ─────────────────────────────────────────────────────────────
def enviar_telegram(mensaje, exito=True):
    """Envía una notificación formateada a Telegram"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    # Si faltan credenciales, solo loguea y continúa
    if not token or not chat_id:
        print("⚠️ Telegram: credenciales no configuradas (revisa GitHub Secrets)")
        return
    
    emoji = "✅" if exito else "❌"
    texto = f"{emoji} *Mimarca Scraper*\n\n{mensaje}"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": texto,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("📱 Notificación enviada a Telegram")
        else:
            print(f"⚠️ Error Telegram API: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"⚠️ Excepción al enviar a Telegram: {str(e)}")


# ─────────────────────────────────────────────────────────────
# FUNCIÓN: Scraping principal
# ─────────────────────────────────────────────────────────────
def scraper_basico():
    """Extrae datos de books.toscrape.com y guarda en CSV"""
    url = "http://books.toscrape.com/"
    print(f"🔍 Conectando a {url}...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    productos = soup.find_all('article', class_='product_pod')
    
    if not productos:
        raise Exception("No se encontraron productos en la página")
    
    # Preparar archivo CSV
    archivo = 'resultados.csv'
    existe = os.path.isfile(archivo)
    datos_guardados = []
    
    with open(archivo, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Escribir cabecera si es la primera vez
        if not existe:
            writer.writerow(['Fecha', 'Titulo', 'Precio', 'Disponibilidad', 'URL'])
        
        # Procesar cada producto (limitamos a 5 para prueba rápida)
        for i, producto in enumerate(productos[:5]):
            try:
                fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                titulo = producto.h3.a['title']
                precio = producto.find('p', class_='price_color').text
                disponibilidad = producto.find('p', class_='instock availability').text.strip()
                
                # Construir URL relativa
                link_rel = producto.h3.a['href']
                url_completa = f"{url}{link_rel}" if not link_rel.startswith('http') else link_rel
                
                writer.writerow([fecha, titulo, precio, disponibilidad, url_completa])
                datos_guardados.append({'titulo': titulo, 'precio': precio})
                
                print(f"✅ [{i+1}/5] {titulo} - {precio}")
                
            except Exception as e:
                print(f"⚠️ Error procesando producto: {str(e)}")
                continue
    
    print(f"\n📊 Total procesados: {len(datos_guardados)}")
    print(f"💾 Datos guardados en {archivo}")
    
    return datos_guardados


# ─────────────────────────────────────────────────────────────
# FUNCIÓN: Generar resumen para Telegram
# ─────────────────────────────────────────────────────────────
def generar_resumen(datos):
    """Crea un mensaje resumen con los primeros resultados"""
    if not datos:
        return "⚠️ No se extrajeron datos"
    
    lineas = [f"📚 *Libros procesados:* `{len(datos)}`\n"]
    
    # Mostrar los primeros 3 como preview
    for item in datos[:3]:
        lineas.append(f"• *{item['titulo']}* → {item['precio']}")
    
    if len(datos) > 3:
        lineas.append(f"_... y {len(datos) - 3} más_")
    
    lineas.append(f"\n🕐 {datetime.datetime.now().strftime('%d/%m %H:%M')}")
    lineas.append(f"🔗 [Ver repo](https://github.com/{os.getenv('GITHUB_REPOSITORY', '')})")
    
    return "\n".join(lineas)


# ─────────────────────────────────────────────────────────────
# BLOQUE PRINCIPAL
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("🚀 Iniciando Mimarca Scraper...")
    print(f"📦 Repo: {os.getenv('GITHUB_REPOSITORY', 'desconocido')}")
    print(f"🔢 Run ID: {os.getenv('GITHUB_RUN_NUMBER', 'N/A')}")
    print("-" * 50)
    
    try:
        # Ejecutar scraping
        datos = scraper_basico()
        
        # Generar y enviar notificación de éxito
        resumen = generar_resumen(datos)
        enviar_telegram(resumen, exito=True)
        
        print("\n🎉 Proceso completado exitosamente")
        
    except Exception as e:
        # Notificar error y propagar para que GitHub Actions falle
        error_msg = f"⚠️ *Error en scraping:*\n\n`{str(e)}`\n\n🔍 Revisa los logs en Actions."
        enviar_telegram(error_msg, exito=False)
        print(f"\n❌ Error crítico: {str(e)}")
        raise
