import pandas as pd
import json
import os # ¡Asegúrate que esta línea esté presente para la corrección de ruta!

# Variable global: ESTA LÍNEA SOLUCIONA EL 'NameError'
ESTADO_JUEGO_FILE = 'akinator_carros_estado.json' 

def cargar_estado_juego(filename):
    """Carga el árbol de decisiones y la lista de carros desde un archivo JSON."""
# ... (El resto del código)
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('arbol', {}), data.get('carros', [])
    except FileNotFoundError:
        # ESTE BLOQUE DEBE ESTAR IDENTADO
        print("No se encontró un estado de juego previo. Se inicializará con los datos del CSV.")
        return None, None
    except json.JSONDecodeError:
        # ESTE BLOQUE DEBE ESTAR IDENTADO
        print("Error al decodificar el archivo de estado. Se inicializará con los datos del CSV.")
        return None, None
def guardar_estado_juego(arbol, carros, filename):
    """Guarda el árbol de decisiones y la lista de carros en un archivo JSON."""
    data = {'arbol': arbol, 'carros': carros}
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("\n¡Estado del juego guardado!")

def inicializar_arbol_desde_csv(file_path):
    """
    Inicializa el árbol de decisiones y la lista de carros desde el CSV.
    Asume una estructura de 5 niveles con preguntas y respuestas para llegar
    a una lista de carros.
    """
    # Leer solo las primeras filas que contienen la estructura y la fila de carros
    try:
        df = pd.read_csv(file_path, header=None, encoding='utf-8', keep_default_na=False)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{file_path}'")
        return None, None
    except Exception as e:
        print(f"Error al leer el CSV: {e}")
        return None, None

    # El árbol se representará como un diccionario anidado
    # {pregunta: {'si': {pregunta/carro}, 'no': {pregunta/carro}}}
    arbol = {}
    carros = []
    
    # La lógica de mapeo es compleja por la estructura "ancha" del CSV
    # Se crea un mapeo directo basado en el 'snippet' que identifica la celda del carro
    
    # 1. Identificar la fila de carros (fila 5 en el índice 0, o 'Nivel 5' + 2)
    fila_carros = df.iloc[5]
    
    # 2. Inicializar el árbol con la pregunta del Nivel 1 (A2)
    pregunta_nivel_1 = df.iloc[0, 1]
    arbol = {'pregunta': pregunta_nivel_1, 'si': {}, 'no': {}}

    # 3. Mapear los caminos de 'si' y 'no' y preguntas
    # Nota: Este mapeo es una simplificación forzada basada en el 'snippet'
    # y las 5 preguntas. En un CSV real, se requeriría un parser más robusto.

    # Camino SI (Tracción Delantera)
    # Nivel 2: ¿Es Estado Unidense? (C3)
    arbol['si'] = {'pregunta': df.iloc[2, 2], 'si': {}, 'no': {}}
    
    # Nivel 3: (C3 -> SI) ¿Es de la marca Ford? (C4)
    arbol['si']['si'] = {'pregunta': df.iloc[3, 3], 'si': {}, 'no': {}}
    # Nivel 3: (C3 -> NO) ¿Es Japones? (C8)
    arbol['si']['no'] = {'pregunta': df.iloc[3, 7], 'si': {}, 'no': {}}

    # Nivel 4 (Camino más largo, ej: SI -> SI -> SI)
    # C4->SI: ¿Su motor es en linea? (C5)
    arbol['si']['si']['si'] = {'pregunta': df.iloc[4, 4], 'si': {}, 'no': {}}
    
    # Nivel 5 (ej: SI -> SI -> SI -> SI): ¿Es de 4 Cilindros? (C6) -> Carro (C7)
    # El carro estará en la fila 5, columna 6 (índice 5).
    # Como los carros están en las celdas C6, C8, C10... se ajusta la extracción.

    def get_carro_at_path(path_indices):
        """Busca el carro en la fila 5 basado en el índice de la columna final."""
        # Los carros están en la fila 5 (índice 5), en las columnas (índice) 1, 3, 5, 7, 9...
        # La lógica es que la columna del carro es 2 * (nivel 5 index) - 1.
        # Por simplicidad, se busca la primera celda no vacía después del camino.
        
        # Ejemplo: El primer carro (Ford Fiesta) está en la columna 1
        # El segundo (Ford Focus) en la 3.
        # El tercer (Chevrolet Chevy Pop) en la 5.
        # Esto requiere una lógica de mapeo columna-carro muy específica del CSV.
        
        # Mapeo manual de la primera columna de carros por ruta para iniciar
        if path_indices == [0, 0, 0, 0]: # Si->Si->Si->Si (Tracc. Delantera, USA, Ford, En linea)
            carro = df.iloc[5, 1] # Ford Fiesta USA I4 TD
        elif path_indices == [0, 0, 0, 1]: # Si->Si->Si->No (Tracc. Delantera, USA, Ford, NO En linea)
            carro = df.iloc[5, 3] # Ford Focus RS USA Ecoboost I4 TA
        else: # Placeholder para el resto
            carro = fila_carros[path_indices[-1] * 2 + 1]
            if not isinstance(carro, str) or carro.strip() == '':
                 carro = "Carro no especificado en el CSV"
        
        if isinstance(carro, str) and carro.strip():
            carros.append(carro.strip())
            return carro.strip()
        return "Carro Desconocido - Fin del camino"


    # Estructura del árbol inicial (limitado para no hacer el mapeo de 30 columnas a mano)
    arbol = {
        'pregunta': '¿Es Traccion Delantera?',
        'si': {
            'pregunta': '¿Es Estado Unidense?',
            'si': {
                'pregunta': '¿Es de la marca Ford?',
                'si': {
                    'pregunta': '¿Su motor es en linea?',
                    'si': get_carro_at_path([0,0,0,0]), # Ford Fiesta
                    'no': get_carro_at_path([0,0,0,1])  # Ford Focus
                },
                'no': get_carro_at_path([0,0,1]) # Chevrolet Chevy Pop
            },
            'no': get_carro_at_path([0,1]) # Nissan 240Z
        },
        'no': {
            'pregunta': '¿Es Traccion Trasera?',
            'si': {
                'pregunta': '¿Es Estado Unidense?',
                'si': get_carro_at_path([1,0]), # Shelby Cobra
                'no': get_carro_at_path([1,1]) # Mazda Miata
            },
            'no': get_carro_at_path([1,2]) # Bugatti Chiron SS
        }
    }
    
    # Limpieza de carros agregados (la función get_carro_at_path los agregó)
    carros_final = list(set([c for c in carros if c.strip() and "Desconocido" not in c]))

    return arbol, carros_final

def jugar(arbol_actual, carros_disponibles):
    """Inicia el juego Akinator recorriendo el árbol."""
    
    if isinstance(arbol_actual, str):
        # Es un carro (hoja del árbol)
        print(f"\n¡Creo que es el **{arbol_actual}**!")
        respuesta = input("¿Adiviné? (s/n): ").lower()
        
        if respuesta == 's':
            print("¡Soy el mejor Akinator de carros! 🥳")
            return arbol_actual, True # Devuelve el carro adivinado y éxito
        else:
            print("¡Rayos! Necesito aprender.")
            # Fase de aprendizaje
            nuevo_carro = input("¿Qué carro era? (Ej: Ferrari F40 Italiano V8 TT): ").strip()
            nueva_pregunta = input(f"Dame una pregunta S/N que diferencie '{nuevo_carro}' de '{arbol_actual}': ").strip()
            
            # Pregunta para el nuevo carro
            resp_nuevo_carro = input(f"Para el carro '{nuevo_carro}', la respuesta a '{nueva_pregunta}' es (s/n): ").lower()
            
            # La nueva pregunta reemplaza la hoja actual
            nuevo_nodo = {
                'pregunta': nueva_pregunta,
                'si': nuevo_carro if resp_nuevo_carro == 's' else arbol_actual,
                'no': arbol_actual if resp_nuevo_carro == 's' else nuevo_carro
            }
            
            # Asegurar que el nuevo carro se añada a la lista global
            if nuevo_carro not in carros_disponibles:
                carros_disponibles.append(nuevo_carro)
            
            return nuevo_nodo, False # Devuelve el nuevo nodo para reemplazar la hoja en el árbol, y fallo
            
    else:
        # Es un nodo de pregunta (rama del árbol)
        pregunta = arbol_actual['pregunta']
        respuesta = input(f"\nPregunta: **{pregunta}** (s/n): ").lower()
        
        if respuesta == 's':
            clave = 'si'
        elif respuesta == 'n':
            clave = 'no'
        else:
            print("Respuesta no válida. Inténtalo de nuevo.")
            return arbol_actual, False
        
        # Recursión: Sigue al siguiente nodo y actualiza el hijo si hay aprendizaje
        resultado, adivinado = jugar(arbol_actual[clave], carros_disponibles)
        
        if not adivinado and isinstance(arbol_actual[clave], str):
            # Si falló la adivinanza y el hijo era un carro (hoja)
            arbol_actual[clave] = resultado
            return arbol_actual, False
        
        return arbol_actual, adivinado

def main():
    """Función principal del Akinator."""
    
    # 1. Cargar estado o inicializar
    arbol, carros = cargar_estado_juego(ESTADO_JUEGO_FILE)
    
    if arbol is None:
        print("Inicializando el árbol de decisiones a partir de 'Akinnator carros.xlsx - Hoja1.csv'...")
        arbol, carros = inicializar_arbol_desde_csv("Akinnator carros.xlsx - Hoja1.csv")

    if not arbol:
        print("No se pudo inicializar el juego. Saliendo.")
        return

    while True:
        print("\n" + "="*50)
        print("🤖 **¡Bienvenido al Akinator de Carros!** 🏁")
        print("Piensa en uno de los carros de nuestra lista y yo lo adivinaré.")
        print("Responde con 's' (sí) o 'n' (no).")
        print("="*50)
        
        # Clonar el árbol y la lista para que las modificaciones sean visibles
        # solo si el juego finaliza y se guarda
        arbol_copia = json.loads(json.dumps(arbol))
        carros_copia = list(carros)
        
        arbol_final, adivinado = jugar(arbol_copia, carros_copia)

        if not adivinado:
            # Reemplazar el árbol viejo con el nuevo que incluye el aprendizaje
            arbol = arbol_final
            carros = carros_copia
            guardar_estado_juego(arbol, carros, ESTADO_JUEGO_FILE)
        
        # Preguntar si quiere jugar de nuevo
        jugar_otra_vez = input("\n¿Quieres jugar de nuevo? (s/n): ").lower()
        if jugar_otra_vez != 's':
            print("¡Adiós! Gracias por enseñarme más sobre carros.")
            break

if __name__ == "__main__":
    main()