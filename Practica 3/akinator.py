import pandas as pd
import json
import os 
# Asegúrate de haber instalado 'openpyxl' para que pd.read_excel funcione

# 1. VARIABLES GLOBALES
ESTADO_JUEGO_FILE = 'akinator_carros_estado.json' 
# *** CORRECCIÓN CRÍTICA: Nombre del archivo basado en ls -l ***
CSV_FILE_PATH = 'Akinnator carros.xlsx' 

# 2. FUNCIONES PARA GESTIONAR EL ESTADO DEL JUEGO (APRENDIZAJE)

def cargar_estado_juego(filename):
    """Carga el árbol de decisiones y la lista de carros desde un archivo JSON."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('arbol', {}), data.get('carros', [])
    except FileNotFoundError:
        print("No se encontró un estado de juego previo. Se inicializará con los datos del CSV.")
        return None, None
    except json.JSONDecodeError:
        print("Error al decodificar el archivo de estado. Se inicializará con los datos del CSV.")
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

    print(f"Buscando archivo en: {ruta_completa_archivo}")

    try:
        # *** CORRECCIÓN CRÍTICA: USAR read_excel ***
        # Se asume que la hoja de datos se llama 'Hoja1', si tiene otro nombre, cámbialo aquí.
        df = pd.read_excel(ruta_completa_archivo, header=None, sheet_name='Hoja1', keep_default_na=False)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{file_path}' en la ubicación esperada.")
        return None, None
    except ImportError:
        print("Error de dependencia: La biblioteca 'openpyxl' es necesaria para leer archivos .xlsx. Instálala con 'pip install openpyxl'")
        return None, None
    except Exception as e:
        print(f"Error al leer el archivo (posiblemente un problema con la hoja de cálculo): {e}")
        return None, None

    arbol = {}
    carros = []
    
    def get_carro_at_path(path_indices):
        """Busca el carro en la fila 5 (índice 5) basada en la lógica del Excel."""
        
        if path_indices == [0, 0, 0, 0]: 
            carro = df.iloc[5, 1] # Ford Fiesta USA I4 TD
        elif path_indices == [0, 0, 0, 1]: 
            carro = df.iloc[5, 3] # Ford Focus RS USA Ecoboost I4 TA
        elif path_indices == [0, 0, 1]: 
            carro = df.iloc[5, 5] # Chevrolet Chevy Pop USA I4 TD
        elif path_indices == [0, 1]: 
            carro = df.iloc[5, 9] # Nissan Fairlady Z 240Z Japones L24 I6 TT
        elif path_indices == [1, 0]: 
            carro = df.iloc[5, 7] # Shelby AC Cobra USA 427 V8 TT
        elif path_indices == [1, 1]: 
            carro = df.iloc[5, 3] # Mazda Miata Mx-5 Japones Skyactiv G I4 TT (Nota: Mismo índice por simplificación)
        elif path_indices == [1, 2]: 
            carro = df.iloc[5, 11] # Bugatti Chiron SS Frances W16 TA
        else:
            return "Carro Desconocido - Fin del camino"

        if isinstance(carro, str) and carro.strip():
            carros.append(carro.strip())
            return carro.strip()
        return "Carro Desconocido - Fin del camino"


    arbol = {
        'pregunta': df.iloc[0, 1],
        'si': {
            'pregunta': df.iloc[2, 1],
            'si': {
                'pregunta': df.iloc[3, 1],
                'si': {
                    'pregunta': df.iloc[4, 1],
                    'si': get_carro_at_path([0,0,0,0]),
                    'no': get_carro_at_path([0,0,0,1])
                },
                'no': get_carro_at_path([0,0,1])
            },
            'no': get_carro_at_path([0,1])
        },
        'no': {
            'pregunta': df.iloc[2, 9],
            'si': {
                'pregunta': df.iloc[3, 9],
                'si': get_carro_at_path([1,0]),
                'no': get_carro_at_path([1,1])
            },
            'no': get_carro_at_path([1,2])
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
        pregunta = arbol_actual['pregunta']
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
        # Llama a la función actualizada que lee XLSX
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