"""
Akinator de carros (versión CLI con opción de volver a jugar)
- No lee Excel en tiempo de ejecución.
- Base de datos embebida con 32 autos.
- Aprende nuevos autos/preguntas.
"""

import json
import os

CARS = [
    "Toyota Supra Japones 2JZ-GTE I6 TT",
    "Chevrolet Camaro USA ZL1 LT4 V8 TT",
    "Volkswagen Beetle Aleman Boxer4 TT",
    "Nissan Skyline GTR Japones R34 RB26DETT L6 TA",
    "Porsche 911 Gt3 RS Aleman Boxer6 TT",
    "Ford F-150 Raptor USA Ecoboost V6 T4",
    "Ford Mustang GT USA Coyote V8 TT",
    "McLaren F1 Britanico V12 TT",
    "Lamborghini Murcielago Italiano V12 TA",
    "Lamborghini Gallardo Italiano V10 TA",
    "Ferrari F-40 Italiano V8 TT",
    "Nissan Tsuru Japones I4 TD",
    "Chevrolet Chevy Pop USA I4 TD",
    "Ford Fiesta USA I4 TD",
    "Ford Focus RS USA Ecoboost I4 TA",
    "Volkswagen Jetta Aleman I4 TD",
    "Dodge Charger R/T 1970 USA Hemi V8 TT",
    "Mitsubishi Lancer Evolution 9 Japones I4 TA",
    "Subaru Impreza STI Japones Boxer4 TA",
    "Chevrolet Impala SS 1994 USA V6 TT",
    "Acura NSX Japones V6 TA",
    "Bugatti Chiron SS Frances W16 TA",
    "Chevrolet Astra USA I4 TD",
    "Toyota Corolla 86 Japones I4 TT",
    "Lamborghini Aventador J Italiano V12 TA",
    "Ferrari La Ferrari Italiano V12 TT",
    "Mazda 3 Japones Sckyactiv G I4 TD",
    "BMW M3 E30 Aleman M20 I6 TT",
    "Mazda Miata Mx-5 Japones Skyactiv G I4 TT",
    "Shelby AC Cobra USA 427 V8 TT",
    "Chevrolet Corvette C6 Z06 USA LT4 V8 TT",
    "Nissan Fairlady Z 240Z Japones L24 I6 TT"
]

QUESTIONS = [
    "¿Es Traccion Delantera?",
    "¿Es Estado Unidense?",
    "¿Es de la marca Ford?",
    "¿Su motor es en linea?",
    "¿Es de 4 Cilindros?",
    "¿Seguro que es Ford?",
    "¿Es de la Marca Chevrolet?",
    "¿Es Coche Hatchback pequeño?",
    "¿Es Japones?",
    "¿Es de la Marca Mazda?",
    "¿Es Hatchback?",
    "¿Es Aleman?",
    "¿Es de Volkswagen?",
    "¿Es Traccion Trasera?",
    "¿Es Chevrolet?",
    "¿Es Un Corvette?",
    "¿Es de Ford?",
    "¿Es Aleman?",
    "¿Es JDM?",
    "¿Es Famoso por los Rallys?"
]

DB_FILE = "learned_db.json"

# ---------------- utilidad ----------------
def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def ask(question):
    while True:
        r = input(question + " (si/no/no sé): ").strip().lower()
        if r in ("si","s","yes","y"):
            return "si"
        if r in ("no","n"):
            return "no"
        if r in ("no sé","nose","ns","no se","idk"):
            return "no se"
        print("Responde 'si', 'no' o 'no sé' por favor.")

# ---------------- filtrado heurístico ----------------
def filter_cars(answers):
    candidates = CARS.copy()

    if answers.get("¿Es Estado Unidense?") == "si":
        candidates = [c for c in candidates if any(k in c for k in ("USA","Chevrolet","Ford","Shelby","Corvette","Camaro","Impala","Dodge"))]

    if answers.get("¿Es Japones?") == "si" or answers.get("¿Es JDM?") == "si":
        candidates = [c for c in candidates if any(k in c for k in ("Japones","Nissan","Toyota","Mazda","Subaru","Mitsubishi","Acura"))]

    if answers.get("¿Es Aleman?") == "si":
        candidates = [c for c in candidates if any(k in c for k in ("Aleman","BMW","Volkswagen","Porsche"))]

    if answers.get("¿Es de la marca Ford?") == "si" or answers.get("¿Es de Ford?") == "si":
        candidates = [c for c in candidates if any(k in c for k in ("Ford","Mustang","F-150"))]

    if answers.get("¿Es de la Marca Chevrolet?") == "si" or answers.get("¿Es Chevrolet?") == "si":
        candidates = [c for c in candidates if any(k in c for k in ("Chevrolet","Camaro","Corvette","Chevy","Impala"))]

    if answers.get("¿Es de Volkswagen?") == "si":
        candidates = [c for c in candidates if "Volkswagen" in c]

    if answers.get("¿Es de la Marca Mazda?") == "si":
        candidates = [c for c in candidates if "Mazda" in c or "Miata" in c]

    if answers.get("¿Es Traccion Delantera?") == "si":
        candidates = [c for c in candidates if any(k in c for k in ("Jetta","Fiesta","Astra","Corolla","Mazda 3","Focus"))]

    if answers.get("¿Es Traccion Trasera?") == "si":
        candidates = [c for c in candidates if any(k in c for k in ("Mustang","Corvette","Supra","Skyline","Fairlady","Cobra","Shelby"))]

    if answers.get("¿Es de 4 Cilindros?") == "si":
        candidates = [c for c in candidates if "I4" in c or "Boxer4" in c]

    if answers.get("¿Su motor es en linea?") == "si":
        candidates = [c for c in candidates if "I6" in c or "I4" in c or "L24" in c]

    if answers.get("¿Es Famoso por los Rallys?") == "si":
        candidates = [c for c in candidates if any(k in c for k in ("Impreza","Lancer","Evolution","Subaru","Mitsubishi"))]

    db = load_db()
    for rule in db.get("rules", []):
        q = rule.get("question")
        ans = rule.get("answer")
        car = rule.get("car")
        if answers.get(q) == ans:
            candidates = [c for c in candidates if car.lower() in c.lower()]

    return candidates

def guess(candidates):
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]
    print("\nTengo varios candidatos:")
    for i, c in enumerate(candidates, 1):
        print(f"{i}. {c}")
    choice = input("Elige el número del auto que tenías en mente, o escribe 0 si ninguno: ").strip()
    try:
        n = int(choice)
        if n == 0:
            return None
        if 1 <= n <= len(candidates):
            return candidates[n-1]
    except:
        pass
    return None

# ---------------- aprendizaje ----------------
def learn(db, asked_answers):
    print("\nNo lo adiviné. Enséñame para la próxima.")
    real = input("¿Qué auto tenías en mente? Escribe el nombre exacto: ").strip()
    if not real:
        print("Nombre vacío — no guardo nada.")
        return db
    q = input("Dame una pregunta de sí/no que distinga ese auto de los demás: ").strip()
    if not q:
        db.setdefault("autos_extra", []).append(real)
        save_db(db)
        print("Guardé el auto en la base de datos (sin pregunta).")
        return db
    ans = ""
    while ans not in ("si","no"):
        ans = input(f"Para '{real}', ¿la respuesta a '{q}' es si o no?: ").strip().lower()
    db.setdefault("rules", []).append({"question": q, "answer": ans, "car": real})
    db.setdefault("autos_extra", []).append(real)
    save_db(db)
    print("¡Listo! Aprendí ese auto y su pregunta. 🚗💡")
    return db

# ---------------- flujo principal ----------------
def play_once():
    db = load_db()
    answers = {}
    print("\nResponde con 'si', 'no' o 'no sé'.\n")

    for q in QUESTIONS:
        a = ask(q)
        answers[q] = a
        candidates = filter_cars(answers)
        if len(candidates) <= 3:
            g = guess(candidates)
            if g:
                print("\n¡Lo adiviné! 🎯 ->", g)
            else:
                learn(db, answers)
            return

    candidates = filter_cars(answers)
    g = guess(candidates)
    if g:
        print("\n¡Lo adiviné! 🎯 ->", g)
    else:
        learn(db, answers)

def main():
    print("=== Akinator de Carros ===")
    print("Versión CLI con aprendizaje automático.\n(No leo Excel, lo prometo.)")

    while True:
        play_once()
        print("\n¿Quieres jugar otra vez o salir?")
        print("1. Adivinar otro auto")
        print("2. Salir")
        choice = input("Selecciona una opción (1/2): ").strip()
        if choice == "1":
            continue
        else:
            print("\nGracias por jugar al Akinator de Carros. ¡Hasta la próxima! 👋")
            break

if __name__ == "__main__":
    main()
