import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from knowledge_acquisition import KnowledgeAcquisition

class KnowledgeChatbot:
    def __init__(self):
        self.knowledge = KnowledgeAcquisition()
        print("🤖 Sistema de Adquisición de Conocimiento Inicializado")
        print(f"💾 Base de conocimiento: {sum(len(v) for v in self.knowledge.knowledge.values())} items")
    
    def start_chat(self):
        """Inicia el chat interactivo de adquisición de conocimiento"""
        print("\n" + "="*60)
        print("           SISTEMA DE ADQUISICIÓN DE CONOCIMIENTO")
        print("="*60)
        print("Escribe 'salir' para terminar la conversación\n")
        print("¡Hola! Soy un sistema que aprende contigo. Puedes enseñarme")
        print("cualquier tema preguntándome sobre ello.\n")
        
        while True:
            try:
                user_input = input("👤 Tú: ").strip()
                
                if user_input.lower() in ['salir', 'exit', 'quit', 'adios']:
                    print("🤖 ¡Gracias por enseñarme! Hasta pronto. 📚")
                    break
                
                response = self.get_response(user_input)
                print(f"🤖 Sistema: {response}")
                
            except KeyboardInterrupt:
                print("\n🤖 Conversación interrumpida. ¡Hasta pronto!")
                break
            except Exception as e:
                print(f"🤖 Error: {e}")
    
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