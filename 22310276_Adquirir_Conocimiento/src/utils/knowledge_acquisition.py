import json
import os
from typing import Dict, Any

class KnowledgeAcquisition:
    def __init__(self, knowledge_file: str = "src/chatbot/knowledge_base.json"):
        self.knowledge_file = knowledge_file
        self.knowledge = self.load_knowledge()
    
    def load_knowledge(self) -> Dict[str, Any]:
        """Carga la base de conocimiento desde el archivo JSON"""
        try:
            with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"conversaciones": {}, "temas_generales": {}}
    
    def save_knowledge(self):
        """Guarda la base de conocimiento en el archivo JSON"""
        os.makedirs(os.path.dirname(self.knowledge_file), exist_ok=True)
        with open(self.knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge, f, ensure_ascii=False, indent=2)
    
    def find_answer(self, question: str) -> str:
        """Busca una respuesta en la base de conocimiento"""
        question_lower = question.lower()
        
        # Buscar en conversaciones
        for key, answer in self.knowledge["conversaciones"].items():
            if key in question_lower:
                return answer
        
        # Buscar en temas generales
        for topic, info in self.knowledge["temas_generales"].items():
            if topic in question_lower:
                return info
        
        return None
    
    def acquire_new_knowledge(self, question: str) -> str:
        """Adquiere nuevo conocimiento cuando no se encuentra respuesta"""
        print(f"\n🤖 No tengo información sobre: '{question}'")
        print("💡 ¡Ayúdame a aprender! Por favor completa la información:")
        
        category = input("¿Categoría? (conversaciones/temas_generales): ").lower()
        key_word = input("¿Palabra clave para recordar? (ej: 'python', 'base de datos'): ").lower()
        answer = input("¿Información completa? (explica detalladamente): ")
        
        if category in self.knowledge:
            self.knowledge[category][key_word] = answer
            self.save_knowledge()
            return f"✅ ¡Gracias! He aprendido sobre '{key_word}'. ¿En qué más puedo ayudarte?"
        else:
            return "❌ Categoría no válida. Use: conversaciones o temas_generales."