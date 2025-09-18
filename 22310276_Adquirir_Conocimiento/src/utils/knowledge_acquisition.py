import json
import os
from typing import Dict, Any

class KnowledgeAcquisition:
    def __init__(self, knowledge_file: str = "knowledge_base.json"):
        self.knowledge_file = knowledge_file
        self.knowledge = self.load_knowledge()
    
    def load_knowledge(self) -> Dict[str, Any]:
        """Carga el conocimiento desde el archivo JSON"""
        if os.path.exists(self.knowledge_file):
            try:
                with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return self._create_default_knowledge()
        else:
            return self._create_default_knowledge()
    
    def _create_default_knowledge(self) -> Dict[str, Any]:
        """Crea una base de conocimiento por defecto"""
        return {
            "conversaciones": {
                "hola": "¡Hola! ¿En qué puedo ayudarte hoy?",
                "adiós": "¡Hasta luego! Fue un placer ayudarte.",
                "gracias": "¡De nada! Estoy aquí para ayudarte cuando lo necesites."
            },
            "temas_generales": {
                "tiempo": "El tiempo es una magnitud física con la que medimos la duración de los eventos.",
                "universo": "El universo es todo lo que existe: materia, energía, espacio y tiempo."
            },
            "tecnologia": {
                "python": "Python es un lenguaje de programación interpretado de alto nivel y propósito general.",
                "inteligencia artificial": "La IA es la simulación de procesos de inteligencia humana por máquinas."
            }
        }
    
    def save_knowledge(self) -> None:
        """Guarda el conocimiento en el archivo JSON"""
        try:
            with open(self.knowledge_file, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Error al guardar el conocimiento: {e}")
    
    def acquire_new_knowledge(self, question: str) -> str:
        """Adquiere nuevo conocimiento cuando no se encuentra respuesta"""
        print(f"\n🤖 No tengo información sobre: '{question}'")
        print("💡 ¡Ayúdame a aprender! Por favor completa la información:")
        
        # Mostrar categorías existentes
        print(f"\n📂 Categorías existentes: {', '.join(self.knowledge.keys())}")
        
        while True:
            category = input("¿Categoría? (puedes usar una existente o crear nueva): ").lower().strip()
            
            if not category:
                print("❌ La categoría no puede estar vacía. Intenta de nuevo.")
                continue
                
            # Normalizar categorías (manejar typos y plurales)
            category_normalized = self.normalize_category(category)
            
            if category_normalized:
                break
            else:
                print("❌ Categoría no válida. Intenta de nuevo.")
        
        key_word = input("¿Palabra clave para recordar? (ej: 'python', 'base de datos'): ").lower().strip()
        
        if not key_word:
            return "❌ La palabra clave no puede estar vacía."
        
        answer = input("¿Información completa? (explica detalladamente): ").strip()
        
        if not answer:
            return "❌ La información no puede estar vacía."
        
        # Agregar nuevo conocimiento
        if category_normalized not in self.knowledge:
            self.knowledge[category_normalized] = {}
        
        self.knowledge[category_normalized][key_word] = answer
        self.save_knowledge()
        
        return f"✅ ¡Excelente! He aprendido sobre '{key_word}' en la categoría '{category_normalized}'. ¿En qué más puedo ayudarte?"

    def normalize_category(self, category: str) -> str:
        """Normaliza las categorías para manejar typos y variaciones"""
        category = category.lower().strip()
        
        # Mapeo de variaciones a categorías estándar
        variations = {
            'conversacion': 'conversaciones',
            'conversaciones': 'conversaciones',
            'charla': 'conversaciones',
            'dialogo': 'conversaciones',
            'saludo': 'conversaciones',
            
            'tema': 'temas_generales', 
            'temas': 'temas_generales',
            'general': 'temas_generales',
            'generales': 'temas_generales',
            'conocimiento': 'temas_generales',
            'info': 'temas_generales',
            
            'tecnologia': 'tecnologia',
            'tecno': 'tecnologia',
            'tech': 'tecnologia',
            
            'ciencia': 'ciencia',
            'cientifico': 'ciencia',
            
            'naturaleza': 'naturaleza',
            'natural': 'naturaleza',
            'medio ambiente': 'naturaleza',
            
            'deporte': 'deportes',
            'deportes': 'deportes',
            'ejercicio': 'deportes',
            
            'arte': 'arte',
            'cultural': 'arte',
            'musica': 'arte',
            
            'historia': 'historia',
            'historico': 'historia'
        }
        
        # Si la categoría ya existe, usarla
        if category in self.knowledge:
            return category
        
        # Buscar variaciones
        if category in variations:
            return variations[category]
        
        # Si es una categoría nueva, crearla (solo si tiene sentido)
        if len(category) >= 3:  # Evitar categorías muy cortas
            # Preguntar si quiere crear nueva categoría
            crear_nueva = input(f"¿Crear nueva categoría '{category}'? (s/n): ").lower().strip()
            if crear_nueva in ['s', 'si', 'sí', 'yes', 'y']:
                return category
        
        return ""

    def search_knowledge(self, question: str) -> str:
        """Busca conocimiento en la base de datos"""
        question_lower = question.lower()
        
        # Buscar en todas las categorías
        for category, topics in self.knowledge.items():
            for topic, answer in topics.items():
                if topic in question_lower:
                    return answer
        
        # Si no se encuentra, adquirir nuevo conocimiento
        return self.acquire_new_knowledge(question)