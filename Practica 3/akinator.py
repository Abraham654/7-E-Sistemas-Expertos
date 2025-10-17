import json
import os

# 1. VARIABLES GLOBALES
ESTADO_JUEGO_FILE = 'akinator_carros_estado.json' 

# 2. BASE DE DATOS INICIAL (La estructura de preguntas se define aquí)
# El valor de una 'hoja' del árbol debe ser un vehículo (str) o el marcador de fin de rama.
MARCADOR_FIN_DE_RAMA = "Carro Desconocido - Fin del camino"

# Estructura del árbol inicial de 5 niveles, completada para cubrir varias ramas.
# Esta estructura reemplaza la necesidad de leer las preguntas del Excel.
ARBOL_INICIAL_ESTRUCTURADO = {
    'pregunta': '¿El carro tiene Tracción Delantera (TD)?',
    'si': { # Rama TD (SI)
        'pregunta': '¿Es un carro de origen Estado Unidense (USA)?',
        'si': { # Rama TD -> USA (SI)
            'pregunta': '¿Es de la marca Ford?',
            'si': { # Rama TD -> USA -> Ford (SI)
                'pregunta': '¿El motor es de 4 Cilindros en línea (I4)?',
                'si': 'Ford Fiesta (TD, USA, I4)',
                'no': 'Ford Focus RS (TD, USA, TA, 4x4)' # Asumo que NO I4 en esta rama es otro Ford conocido
            },
            'no': { # Rama TD -> USA -> NO Ford (Chevrolet, Dodge)
                'pregunta': '¿Es de la marca Chevrolet?',
                'si': 'Chevrolet Chevy Pop (TD, USA, I4)',
                'no': MARCADOR_FIN_DE_RAMA # Otros USA TD
            }
        },
        'no': { # Rama TD -> NO USA (Japón, Alemania, etc.)
            'pregunta': '¿Es de origen Japonés?',
            'si': 'Honda Civic (TD, JAP, I4)',
            'no': 'Volkswagen Golf (TD, ALE, I4)' # Asumo que NO Japonés es Europeo conocido
        }
    },
    'no': { # Rama NO TD (Tracción Trasera, Total, o Central) (NO)
        'pregunta': '¿El carro es predominantemente Tracción Trasera (TT)?',
        'si': { # Rama TT (SI)
            'pregunta': '¿Es un muscle car o deportivo clásico USA?',
            'si': 'Shelby AC Cobra (TT, USA, V8)',
            'no': 'Mazda MX-5 Miata (TT, JAP, I4)'
        },
        'no': { # Rama NO TT (Total/Central)
            'pregunta': '¿Tiene más de 8 cilindros?',
            'si': 'Bugatti Chiron SS (TA, FR, W16)',
            'no': 'Audi R8 (TA, ALE, V10)'
        }
    }
}

# La lista de vehículos se extrae automáticamente del ARBOL_INICIAL_ESTRUCTURADO.
# Si quieres añadir más vehículos sin modificar el árbol, añádelos aquí.
VEHICULOS_INICIALES_JSON = [
    'Ford Fiesta (TD, USA, I4)',
    'Ford Focus RS (TD, USA, TA, 4x4)',
    'Chevrolet Chevy Pop (TD, USA, I4)',
    'Honda Civic (TD, JAP, I4)',
    'Volkswagen Golf (TD, ALE, I4)',
    'Shelby AC Cobra (TT, USA, V8)',
    'Mazda MX-5 Miata (TT, JAP, I4)',
    'Bugatti Chiron SS (TA, FR, W16)',
    'Audi R8 (TA, ALE, V10)',
    # Puedes agregar más vehículos aquí para la base de datos inicial:
    # 'Nissan 240Z (TT, JAP, I6)',
]

# Función para obtener la lista inicial de vehículos a partir del árbol
def obtener_lista_inicial(arbol, vehiculos_list):
    """Recorre el árbol para obtener la lista de vehículos iniciales."""
    if isinstance(arbol, str):
        if arbol != MARCADOR_FIN_DE_RAMA and arbol not in vehiculos_list:
            vehiculos_list.append(arbol)
        return
    
    obtener_lista_inicial(arbol['si'], vehiculos_list)
    obtener_lista_inicial(arbol['no'], vehiculos_list)


# 3. GESTIÓN DEL ESTADO DEL JUEGO (Aprendizaje)

def cargar_estado_juego(filename):
    """Carga el árbol de decisiones y la lista de carros desde un archivo JSON."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('arbol', ARBOL_INICIAL_ESTRUCTURADO), data.get('carros', VEHICULOS_INICIALES_JSON)
    except FileNotFoundError:
        print("No se encontró un estado de juego previo. Se inicializará con la estructura interna.")
        
        # Inicializar la lista de vehículos a partir del árbol y la lista base
        carros_iniciales = list(set(VEHICULOS_INICIALES_JSON))
        obtener_lista_inicial(ARBOL_INICIAL_ESTRUCTURADO, carros_iniciales)
        
        return ARBOL_INICIAL_ESTRUCTURADO, carros_iniciales
    except json.JSONDecodeError:
        print("Error al decodificar el archivo de estado. Se inicializará con la estructura interna.")
        return ARBOL_INICIAL_ESTRUCTURADO, VEHICULOS_INICIALES_JSON

def guardar_estado_juego(arbol, carros, filename):
    """Guarda el árbol de decisiones y la lista de carros en un archivo JSON."""
    data = {'arbol': arbol, 'carros': carros}
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("\n¡Estado del juego guardado! El Akinator ha aprendido algo nuevo. 🧠")


# 4. FUNCIÓN CENTRAL DEL JUEGO (RECURSIVA)

def jugar(arbol_actual, carros_disponibles):
    """Inicia el juego Akinator recorriendo el árbol."""
    
    if isinstance(arbol_actual, str):
        carro_adivinado = arbol_actual
        
        if carro_adivinado == MARCADOR_FIN_DE_RAMA:
            print("\nEl Akinator se ha quedado sin opciones en esta rama.")
            respuesta = 'n' # Forzar el aprendizaje
        else:
            print(f"\n¡Creo que es el **{carro_adivinado}**!")
            respuesta = input("¿Adiviné? (s/n): ").lower()

        if respuesta == 's':
            print("¡Soy el mejor Akinator de carros! 🥳")
            return arbol_actual, True 
        else:
            print("¡Rayos! Necesito aprender.")
            # Fase de aprendizaje
            nuevo_carro = input("¿Qué carro era?: ").strip()
            
            # Si el Akinator falló en un nodo vacío, el carro a diferenciar es el MARCADOR_FIN_DE_RAMA
            carro_a_diferenciar = MARCADOR_FIN_DE_RAMA if carro_adivinado == MARCADOR_FIN_DE_RAMA else carro_adivinado
            
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
            
    else:
        pregunta = arbol_actual.get('pregunta', 'Error: Pregunta no definida')
        
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
    
    # El árbol y los carros se inicializan a partir del JSON o la estructura interna
    arbol, carros = cargar_estado_juego(ESTADO_JUEGO_FILE)

    if not arbol:
        print("Error: No se pudo cargar ni inicializar el árbol de decisiones. Saliendo.")
        return

    while True:
        print("\n" + "="*50)
        print("🤖 **¡Bienvenido al Akinator de Carros!** 🏁")
        print(f"Piensa en un carro ({len(carros)} conocidos). Responde con 's' (sí) o 'n' (no).")
        print("="*50)
        
        # Clonación profunda para evitar modificar el árbol actual antes de guardar
        arbol_copia = json.loads(json.dumps(arbol))
        carros_copia = list(carros)
        
        arbol_final, adivinado = jugar(arbol_copia, carros_copia)

        if not adivinado:
            # Si hubo aprendizaje, actualiza el árbol global y la lista de carros
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