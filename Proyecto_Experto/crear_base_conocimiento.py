import sqlite3

# 1. Conexión a la base de datos (se creará el archivo automovilismo.db)
conn = sqlite3.connect('automovilismo.db')
cursor = conn.cursor()

# 2. Creamos la tabla de Reglas (Hechos -> Conclusión)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reglas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sonido TEXT,
        luces TEXT,
        diagnostico TEXT,
        recomendacion TEXT
    )
''')

# 3. Vaciado del Conocimiento (Aquí están las inferencias pre-programadas)
# Formato: (SÍNTOMA 1, SÍNTOMA 2, DIAGNÓSTICO, RECOMENDACIÓN)
conocimiento = [
    ("silencio", "apagadas", "Batería Muerta o Desconectada", "Revise los bornes de la batería y mida el voltaje con multímetro. Si es 0V, reemplace batería."),
    ("silencio", "encienden", "Falla en el Motor de Arranque (Solenóide)", "Si hay luces pero no hay sonido, el solenoide del arranque está pegado o dañado."),
    ("click", "parpadean", "Batería Descargada (Bajo Amperaje)", "La batería tiene voltaje pero no amperaje. Intente pasar corriente (jump start)."),
    ("click", "encienden", "Falla en Motor de Arranque (Carbones)", "Los carbones del arranque están desgastados. Golpee suavemente el arranque o reemplácelo."),
    ("gira_lento", "tenues", "Batería Agotándose o Alternador Fallando", "El auto apenas tiene energía. Revise si el alternador está cargando correctamente."),
    ("gira_rapido", "encienden", "Falla de Combustible o Chispa", "El motor gira bien (hay batería) pero no explota. Revise bomba de gasolina o bujías.")
]

cursor.executemany('INSERT INTO reglas (sonido, luces, diagnostico, recomendacion) VALUES (?, ?, ?, ?)', conocimiento)

conn.commit()
conn.close()
print("Base de conocimiento 'automovilismo.db' creada con éxito.")