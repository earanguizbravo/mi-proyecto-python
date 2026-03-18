import datetime

def saludar():
    ahora = datetime.datetime.now()
    print(f"¡Hola! El script se ejecutó correctamente a las {ahora.strftime('%H:%M:%S')}")

if __name__ == "__main__":
    saludar()
