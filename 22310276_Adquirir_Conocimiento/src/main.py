from chatbot.engine import KnowledgeChatbot

def main():
    """Función principal del sistema de adquisición de conocimiento"""
    print("Iniciando Sistema de Adquisición de Conocimiento...")
    chatbot = KnowledgeChatbot()
    chatbot.start_chat()

if __name__ == "__main__":
    main()