import pandas as pd
import json
import os 
# Asegúrate de haber instalado 'openpyxl'

# 1. VARIABLES GLOBALES
ESTADO_JUEGO_FILE = 'akinator_carros_estado.json' 
CSV_FILE_PATH = 'Akinnator carros.xlsx' 

# 2. FUNCIONES PARA GESTIONAR EL ESTADO DEL JUEGO (APRENDIZAJE)

def cargar_estado_juego(filename):
    """Carga el árbol de decisiones y la lista de carros desde un archivo JSON."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('arbol', {}), data.get('carros', [])
    except FileNotFoundError:
        print("No se encontró un estado de juego previo. Se inicializará con los datos del Excel.")
        return None, None
    except json.JSONDecodeError:
        print("Error al decodificar el archivo de estado. Se inicializará con los datos del Excel.")
        return None, None

def guardar_estado_juego(arbol, carros, filename):
    """Guarda el árbol de decisiones y la lista de carros en un archivo JSON."""
    data = {'arbol': arbol, 'carros': carros}
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("\n¡Estado del juego guardado! El Akinator ha aprendido algo nuevo. 🧠")

# 3. FUNCIÓN PARA INICIALIZAR EL ÁRBOL DESDE EL ARCHIVO XLSX

def inicializar_arbol_desde_archivo(file_path):
    """
    Inicializa el árbol de decisiones y la lista de carros desde el archivo XLSX,
    corrigiendo los índices de fila para leer solo las preguntas.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_completa_archivo = os.path.join(script_dir, file_path)

    try:
        # Se asume que la hoja de datos se llama 'Hoja1' y el archivo tiene suficientes filas
        df = pd.read_excel(ruta_completa_archivo, header=None, sheet_name='Hoja1', keep_default_na=False)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None, None

    arbol = {}
    carros = []

    # Se usa la Fila 10 (índice 9) del Excel para buscar los carros, asumiendo 5 niveles de preguntas.
    CAR_ROW_INDEX = 10 
    
    def get_carro_at_path(col_index):
        """Busca el carro en la fila de carros (índice 10) en la columna especificada."""
        try:
            # Encuentra el carro en la fila de carros, a partir de la columna del índice dado.
            carro = df.iloc[CAR_ROW_INDEX, col_index] 
        except IndexError:
            return "Carro Desconocido - Fin del camino"

        if isinstance(carro, str) and carro.strip():
            carros.append(carro.strip())
            return carro.strip()
        return "Carro Desconocido - Fin del camino"


    # Estructura del árbol inicial con índices de fila corregidos para las preguntas:
    # Nivel 1 Q: Fila 0
    # Nivel 2 Q: Fila 2
    # Nivel 3 Q: Fila 4 <--- CORRECCIÓN PRINCIPAL (Antes estaba en Fila 3)

    try:
        # Nivel 1 (Fila 0)
        pregunta_1 = df.iloc[0, 1] 

        # Nivel 2 (Fila 2)
        pregunta_2_si = df.iloc[2, 1]     # ¿Es Estado Unidense?
        pregunta_2_no = df.iloc[2, 9]     # ¿Es Traccion Trasera? (Asumiendo que este es el inicio de la rama NO)

        # Nivel 3 (Fila 4)
        pregunta_3_sisi = df.iloc[4, 1]   # ¿Es de la marca Ford? (Si -> Si -> Q)

    except IndexError:
        print("Error: El archivo Excel no tiene suficientes filas o columnas para el mapeo inicial.")
        return None, None

    arbol = {
        'pregunta': pregunta_1, 
        'si': {
            'pregunta': pregunta_2_si,
            'si': {
                'pregunta': pregunta_3_sisi, # Nivel 3: ¿Es de la marca Ford?
                'si': get_carro_at_path(2),    # Carro en columna 2 (Ford Fiesta USA I4 TD)
                'no': get_carro_at_path(4)     # Carro en columna 4 (Ford Focus RS)
            },
            'no': get_carro_at_path(10) # Carro en columna 10 (Nissan 240Z, etc.)
        },
        'no': {
            'pregunta': pregunta_2_no if pregunta_2_no.strip() else '¿Es un auto deportivo?', # CORRECCIÓN: Si la celda es vacía, usa una pregunta por defecto.
            'si': get_carro_at_path(8),  # Shelby AC Cobra
            'no': get_carro_at_path(12)  # Bugatti Chiron SS
        }
    }
    
    carros_final = list(set([c for c in carros if c.strip() and "Desconocido" not in c]))

    return arbol, carros_final

# 4. FUNCIÓN CENTRAL DEL JUEGO (RECURSIVA)
def jugar(arbol_actual, carros_disponibles):
    """Inicia el juego Akinator recorriendo el árbol."""
    
    if isinstance(arbol_actual, str):
        # Es un carro (hoja del árbol)
        print(f"\n¡Creo que es el **{arbol_actual}**!")
        respuesta = input("¿Adiviné? (s/n): ").lower()
        
        if respuesta == 's':
            print("¡Soy el mejor Akinator de carros! 🥳")
            return arbol_actual, True
        else:
            print("¡Rayos! Necesito aprender.")
            # Fase de aprendizaje
            nuevo_carro = input("¿Qué carro era?: ").strip()
            carro_adivinado_mal = arbol_actual
            nueva_pregunta = input(f"Dame una pregunta S/N que diferencie '{nuevo_carro}' de '{carro_adivinado_mal}': ").strip()
            
            resp_nuevo_carro = input(f"Para el carro '{nuevo_carro}', la respuesta a '{nueva_pregunta}' es (s/n): ").lower()
            
            if resp_nuevo_carro == 's':
                si_respuesta = nuevo_carro
                no_respuesta = carro_adivinado_mal
            else:
                si_respuesta = carro_adivinado_mal
                no_respuesta = nuevo_carro
                
            nuevo_nodo = {
                'pregunta': nueva_pregunta,
                'si': si_respuesta,
                'no': no_respuesta
            }
            
            if nuevo_carro not in carros_disponibles:
                carros_disponibles.append(nuevo_carro)
            
            return nuevo_nodo, False
            
    else:
        # Es un nodo de pregunta (rama del árbol)
        pregunta = arbol_actual.get('pregunta', 'Error: Pregunta no definida')
        
        # Manejo de preguntas vacías (como la que te salía ****)
        if not pregunta or pregunta.strip() in ['Si', 'No', '']:
             # Si por alguna razón lee una celda vacía o de respuesta, usa una pregunta por defecto
             pregunta = '¿Es un vehículo de más de 10 años?'
        
        respuesta = input(f"\nPregunta: **{pregunta}** (s/n): ").lower()
        
        if respuesta == 's':
            clave = 'si'
        elif respuesta == 'n':
            clave = 'no'
        else:
            print("Respuesta no válida. Intentemos con 'n' por defecto.")
            clave = 'no'
        
        resultado, adivinado = jugar(arbol_actual[clave], carros_disponibles)
        
        if not adivinado and isinstance(arbol_actual[clave], str):
            arbol_actual[clave] = resultado
            return arbol_actual, False
        
        return arbol_actual, adivinado

# 5. FUNCIÓN PRINCIPAL

def main():
    """Función principal del Akinator."""
    
    arbol, carros = cargar_estado_juego(ESTADO_JUEGO_FILE)
    
    if arbol is None:
        print(f"Inicializando el árbol de decisiones a partir de '{CSV_FILE_PATH}'...")
        arbol, carros = inicializar_arbol_desde_archivo(CSV_FILE_PATH)

    if arbol is None or not arbol:
        print("No se pudo inicializar el juego. Saliendo.")
        return

    while True:
        print("\n" + "="*50)
        print("🤖 **¡Bienvenido al Akinator de Carros!** 🏁")
        print("Piensa en un carro. Responde con 's' (sí) o 'n' (no).")
        print("="*50)
        
        arbol_copia = json.loads(json.dumps(arbol))
        carros_copia = list(carros)
        
        arbol_final, adivinado = jugar(arbol_copia, carros_copia)

        if not adivinado:
            arbol = arbol_final
            carros = carros_copia
            guardar_estado_juego(arbol, carros, ESTADO_JUEGO_FILE)
        
        jugar_otra_vez = input("\n¿Quieres jugar de nuevo? (s/n): ").lower()
        if jugar_otra_vez != 's':
            print("¡Adiós! Gracias por enseñarme más sobre carros.")
            break

# 6. INICIO DEL PROGRAMA
if __name__ == "__main__":
    main()