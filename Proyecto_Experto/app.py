from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Función auxiliar para consultar el motor de inferencia
def consultar_experto(sonido, luces):
    conn = sqlite3.connect('automovilismo.db')
    cursor = conn.cursor()
    
    # Lógica de Inferencia: Buscar coincidencia exacta (Forward Chaining simple)
    query = "SELECT diagnostico, recomendacion FROM reglas WHERE sonido = ? AND luces = ?"
    cursor.execute(query, (sonido, luces))
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado:
        return {"diagnostico": resultado[0], "recomendacion": resultado[1], "exito": True}
    else:
        return {"diagnostico": "Caso no identificado", "recomendacion": "Los síntomas no coinciden con mi base de conocimiento. Consulte un mecánico humano.", "exito": False}

@app.route('/', methods=['GET', 'POST'])
def home():
    resultado = None
    if request.method == 'POST':
        # 1. Obtener hechos del usuario
        s_sonido = request.form.get('sonido')
        s_luces = request.form.get('luces')
        
        # 2. Ejecutar motor de inferencia
        resultado = consultar_experto(s_sonido, s_luces)
        
    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)