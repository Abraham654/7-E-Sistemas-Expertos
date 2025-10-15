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
    Inicializa el árbol de decisiones y la lista de carros desde el archivo XLSX.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_completa_archivo = os.path.join(script_dir, file_path)

    try:
        df = pd.read_excel(ruta_completa_archivo, header=None, sheet_name='Hoja1', keep_default_na=False)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None, None

    arbol = {}
    carros = []

    # Fila donde inician los carros
    CAR_ROW_INDEX = 10 
    
    def get_carro_at_path(col_index):
        """Busca el carro en la fila de carros (índice 10) en la columna especificada."""
        try:
            carro = df.iloc[CAR_ROW_INDEX, col_index] 
        except IndexError:
            return "Carro Desconocido - Fin del camino"

        if isinstance(carro, str) and carro.strip():
            carros.append(carro.strip())
            return carro.strip()
        return "Carro Desconocido - Fin del camino"


    # Estructura del árbol inicial (usando filas 0, 2, 4 para las preguntas)

    try:
        pregunta_1 = df.iloc[0, 1] 
        pregunta_2_si = df.iloc[2, 1]     
        pregunta_2_no = df.iloc[2, 9]     
        pregunta_3_sisi = df.iloc[4, 1]   

    except IndexError:
        print("Error: El archivo Excel no tiene suficientes filas o columnas para el mapeo inicial.")
        return None, None

    arbol = {
        'pregunta': pregunta_1, 
        'si': {
            'pregunta': pregunta_2_si,
            'si': {
                'pregunta': pregunta_3_sisi, 
                'si': get_carro_at_path(2),    
                'no': get_carro_at_path(4)     
            },
            'no': get_carro_at_path(10) 
        },
        'no': {
            'pregunta': pregunta_2_no if pregunta_2_no.strip() else '¿Es un auto deportivo?', 
            'si': get_carro_at_path(8),  
            'no': get_carro_at_path(12)  
        }
    }
    
    carros_final = list(set([c for c in carros if c.strip() and "Desconocido" not in c]))

    return arbol, carros_final

# 4. FUNCIÓN CENTRAL DEL JUEGO (RECURSIVA)

def jugar(arbol_actual, carros_disponibles):
    """Inicia el juego Akinator recorriendo el árbol."""
    
    # ----------------------------------------------------
    # Caso 1: Se ha llegado a una HOJA (un carro o el error 'Desconocido')
    # ----------------------------------------------------
    if isinstance(arbol_actual, str):
        carro_adivinado = arbol_actual
        
        # *** CORRECCIÓN PRINCIPAL: Evitar preguntar si adivinó el mensaje de error ***
        if "Carro Desconocido" in carro_adivinado:
            print("\nEl Akinator se ha quedado sin opciones en esta rama.")
            respuesta = 'n' # Forzar el aprendizaje
        else:
            print(f"\n¡Creo que es el **{carro_adivinado}**!")
            respuesta = input("¿Adiviné? (s/n): ").lower()
        # ----------------------------------------------------

        if respuesta == 's':
            print("¡Soy el mejor Akinator de carros! 🥳")
            return arbol_actual, True 
        else:
            print("¡Rayos! Necesito aprender.")
            # Fase de aprendizaje
            nuevo_carro = input("¿Qué carro era?: ").strip()
            
            # El carro a diferenciar es el que se adivinó (mal)
            carro_a_diferenciar = "un carro genérico" if "Desconocido" in carro_adivinado else carro_adivinado
            
            nueva_pregunta = input(f"Dame una pregunta S/N que diferencie '{nuevo_carro}' de '{carro_a_diferenciar}': ").strip()
            
            resp_nuevo_carro = input(f"Para el carro '{nuevo_carro}', la respuesta a '{nueva_pregunta}' es (s/n): ").lower()
            
            if resp_nuevo_carro == 's':
                si_respuesta = nuevo_carro
                no_respuesta = carro_a_diferenciar
            else:
                si_respuesta = carro_a_diferenciar
                no_respuesta = nuevo_carro
                
            nuevo_nodo = {
                'pregunta': nueva_pregunta,
                'si': si_respuesta,
                'no': no_respuesta
            }
            
            if nuevo_carro not in carros_disponibles:
                carros_disponibles.append(nuevo_carro)
            
            return nuevo_nodo, False 
            
    # ----------------------------------------------------
    # Caso 2: Es un NODO de pregunta
    # ----------------------------------------------------
    else:
        pregunta = arbol_actual.get('pregunta', 'Error: Pregunta no definida')
        
        # *** CORRECCIÓN PRINCIPAL: Evitar la repetición de la pregunta de control ***
        # El problema de la repetición ocurre porque la lógica de 'pregunta no definida'
        # reescribe la variable 'pregunta', pero no cambia el nodo del árbol,
        # causando que el mismo error se repita en la siguiente iteración.
        
        # Lo mejor es confiar en que la pregunta del nodo es correcta
        # y solo corregir la respuesta si no es 's' o 'n'.

        respuesta = input(f"\nPregunta: **{pregunta}** (s/n): ").lower()
        
        if respuesta == 's':
            clave = 'si'
        elif respuesta == 'n':
            clave = 'no'
        else:
            print("Respuesta no válida. Intentemos con 'n' por defecto.")
            clave = 'no'
        
        # La recursión es lo que debe manejar la actualización del árbol
        resultado, adivinado = jugar(arbol_actual[clave], carros_disponibles)
        
        if not adivinado and isinstance(arbol_actual[clave], str):
            # Si falló la adivinanza y el hijo era una hoja, reemplaza la hoja
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