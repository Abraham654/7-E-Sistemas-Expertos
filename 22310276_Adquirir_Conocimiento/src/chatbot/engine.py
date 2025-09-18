import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils.knowledge_acquisition import KnowledgeAcquisition

class KnowledgeChatbot:
    def __init__(self):
        self.knowledge_base = KnowledgeAcquisition()
    
    def start_chat(self):
        """Inicia la conversación con el chatbot"""
        print("🧠 Chatbot de Base de Conocimiento")
        print("=" * 40)
        print("Escribe 'salir' para terminar la conversación\n")
        
        while True:
            user_input = input("👤 Tú: ").strip()
            
            if user_input.lower() in ['salir', 'exit', 'quit', 'adiós']:
                print("🤖: ¡Hasta luego! Fue un placer ayudarte.")
                break
            
            if user_input:
                # AQUÍ DEBE USAR search_knowledge, NO find_answer
                response = self.knowledge_base.search_knowledge(user_input)
                print(f"🤖: {response}")
    
    def get_response(self, question: str) -> str:
        """Obtiene respuesta o adquiere nuevo conocimiento"""
        if not question:
            return "Por favor, hazme una pregunta o cuéntame algo."
        
        # Buscar respuesta existente
        answer = self.knowledge.find_answer(question)
        
        if answer:
            return answer
        else:
            # Adquirir nuevo conocimiento
            return self.knowledge.acquire_new_knowledge(question)