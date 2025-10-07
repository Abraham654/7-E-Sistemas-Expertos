import sys

# La base de datos optimizada (con categorías para manejar los duplicados)
# Clave: Secuencia de respuestas binarias (1=Sí, 0=No)
BASE_DATOS_CARROS = {
    "11111": "Un hipercoche o superdeportivo moderno V12/W16 (Ej: Lamborghini Aventador/Gallardo, Ferrari LaFerrari, Bugatti Chiron).",
    "01111": "Un 'Muscle Car' V8 moderno (Ej: Chevrolet Camaro ZL1, Ford Mustang GT, Corvette C6 Z06).",
    "00100": "Un auto compacto/utilitario FWD (Ej: Nissan Tsuru, Mazda 3, Chevrolet Astra, Ford Fiesta).",
    "00101": "Un deportivo turbo/AWD de 4-6 cilindros moderno (Ej: Toyota Supra, Mazda Miata, Subaru STI, Mitsubishi Evo).",
    "01101": "Una camioneta o SUV deportivo/AWD (Ej: Ford F-150 Raptor, Acura NSX).",
    "11011": "Un superdeportivo V8/V12 icónico pre-2000 (Ej: McLaren F1, Ferrari F-40, Lamborghini Murciélago).",
    "00001": "Un deportivo clásico japonés I6/I4 (Ej: Nissan GTR R34, Toyota Corolla 86, Fairlady Z 240Z).",
    "01011": "Un 'Muscle Car' V8 Clásico (Ej: Dodge Charger R/T, Shelby AC Cobra).",
    "10001": "Un deportivo clásico I6/Boxer Europeo (Ej: BMW M3 E30).",
    "10101": "Un deportivo Boxer moderno (Ej: Porsche 911 GT3 RS).",
    "10100": "Un sedán compacto/europeo moderno (Ej: VW Jetta).",
    "10000": "Un auto icónico de motor trasero (Ej: VW Beetle).",
    # (El resto de las 32 rutas quedarían como "No identificado" o se llenarían con más carros)
}

PREGUNTAS = [
    "1. ¿El carro es originario de Europa (Alemania, Italia, UK, Francia)?",
    "2. ¿Utiliza una configuración de motor V, W o es V12/W16?",
    "3. ¿Es un vehículo relativamente moderno (Lanzado después del año 2000)?",
    "4. ¿El motor tiene 8 o más cilindros (V8, V10, V12, W16)?",
    "5. ¿Es un auto de tracción integral o trasera, pensado para alto rendimiento (NO tracción delantera FWD)?"
]

def obtener_respuesta(pregunta):
    """Solicita una respuesta S/N y la convierte a '1' (Sí) o '0' (No)."""
    while True:
        respuesta = input(f"{pregunta} (S/N): ").strip().upper()
        if respuesta == 'S':
            return '1'
        elif respuesta == 'N':
            return '0'
        else:
            print("Respuesta no válida. Por favor, usa 'S' o 'N'.")

def jugar_akinator_carros():
    print("------------------------------------------")
    print("🚗 AKINATOR DE CARROS (5 PREGUNTAS)")
    print("Piensa en uno de los 32 carros y responde S o N.")
    print("------------------------------------------")

    ruta_respuestas = ""
    
    # Recolectar las 5 respuestas
    for pregunta in PREGUNTAS:
        respuesta_binaria = obtener_respuesta(pregunta)
        ruta_respuestas += respuesta_binaria

    print("\n------------------------------------------")
    print(f"Tu secuencia de respuestas fue: {ruta_respuestas}")
    
    # Buscar el resultado
    resultado = BASE_DATOS_CARROS.get(ruta_respuestas)

    if resultado:
        print(f"\n¡Hecho! El carro en el que pensaste es: \n>>> {resultado} <<<")
    else:
        print("\nLo siento, ese carro no está en nuestra base de datos o su ruta no fue asignada.")
        print("Asegúrate de haber respondido las preguntas con precisión.")
    
    print("------------------------------------------")

# Ejecutar el juego
if __name__ == "__main__":
    jugar_akinator_carros()