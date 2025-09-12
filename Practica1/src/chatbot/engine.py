import os
import sys
from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_core.language_models import BaseLLM
from langchain_core.outputs import LLMResult
from langchain_core.runnables import Runnable
from dotenv import load_dotenv

# Configurar paths
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

# Cargar variables de entorno
load_dotenv()

class MockLLM(Runnable):
    """Mock LLM compatible con LangChain moderno"""
    
    def invoke(self, input: Dict[str, Any], config: Any = None) -> Dict[str, Any]:
        """Método principal para generar respuestas"""
        question = input.get("query", "") or input.get("question", "")
        
        if "aceite" in question.lower():
            response = "El cambio de aceite se recomienda cada 5,000 km o 6 meses. Use aceite 5W-30 sintético para la mayoría de los motores modernos."
        elif "freno" in question.lower() or "pastilla" in question.lower():
            response = "Las pastillas de freno deben revisarse cada 10,000 km y cambiarse cuando el grosor sea menor a 3mm. Los discos de freno suelen durar entre 60,000-80,000 km."
        elif "bujía" in question.lower():
            response = "Las bujías se cambian cada 30,000 km. Síntomas de desgaste incluyen: motor titubea al acelerar, mayor consumo de gasolina y dificultad para arrancar."
        elif "humo" in question.lower() or "azul" in question.lower():
            response = "El humo azul del escape generalmente indica que el motor está quemando aceite. Puede deberse a retenes de válvulas desgastados o anillos de pistón dañados."
        elif "filtro" in question.lower() and "aire" in question.lower():
            response = "El filtro de aire debe revisarse cada 10,000 km y cambiarse cada 20,000 km o si está obstruido. Un filtro sucio reduce la potencia y aumenta el consumo de combustible."
        else:
            response = "Basado en el manual de mecánica automotriz, recomiendo llevar el vehículo a un especialista para un diagnóstico preciso. ¿Puede proporcionar más detalles sobre el problema?"
        
        return {"result": response, "source_documents": []}

class ChatbotEngine:
    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Inicializa el motor del chatbot con la base de conocimiento
        """
        self.persist_directory = persist_directory
        self.vector_store = None
        self.qa_chain = None
        self.setup_engine()
    
    def setup_engine(self):
        """Configura el motor de búsqueda y respuesta"""
        try:
            # 1. Cargar embeddings locales
            embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            
            # 2. Cargar la base de conocimiento vectorial
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=embeddings
            )
            
            print(f"📊 Base de conocimiento cargada: {self.vector_store._collection.count()} documentos")
            
            # 3. Configurar el template para respuestas
            prompt_template = """Eres un experto mecánico automotriz. Responde la pregunta basándote SOLO en el contexto proporcionado.

            Contexto: {context}

            Pregunta: {question}

            Respuesta (sé claro, técnico y conciso):
            """
            
            PROMPT = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
            
            # 4. Usar el mock LLM (compatible con LangChain moderno)
            llm = MockLLM()
            
            # 5. Crear cadena de QA simplificada
            self.qa_chain = lambda x: llm.invoke(x)
            
            print("✅ Motor del chatbot inicializado correctamente")
            
        except Exception as e:
            print(f"❌ Error inicializando el motor: {e}")
            raise
    
    def ask_question(self, question: str) -> Dict:
        """
        Haz una pregunta al chatbot de mecánica
        
        Args:
            question (str): Pregunta del usuario
            
        Returns:
            Dict: Respuesta y documentos fuente
        """
        if not self.qa_chain:
            return {"result": "Error: Motor no inicializado", "source_documents": []}
        
        try:
            result = self.qa_chain({"query": question})
            return {
                "answer": result["result"],
                "sources": result.get("source_documents", [])
            }
        except Exception as e:
            return {"answer": f"Error: {str(e)}", "sources": []}

# Función para pruebas
def test_chatbot():
    """Prueba el chatbot con algunas preguntas"""
    print("🤖 Iniciando chatbot de mecánica...")
    
    chatbot = ChatbotEngine()
    
    # Preguntas de prueba
    test_questions = [
        "¿Cada cuánto debo cambiar el aceite?",
        "¿Qué aceite recomiendan para mi auto?",
        "¿Cada cuánto se cambian las pastillas de freno?",
        "¿Qué significa el humo azul del escape?",
        "¿Cuándo debo cambiar el filtro de aire?",
        "¿Qué pasa si las bujías están desgastadas?"
    ]
    
    for question in test_questions:
        print(f"\n🧑‍💼 Pregunta: {question}")
        response = chatbot.ask_question(question)
        print(f"🤖 Respuesta: {response['answer']}")
        
        if response.get('sources'):
            print("📚 Fuentes utilizadas:")
            for i, doc in enumerate(response['sources'][:2]):
                print(f"   {i+1}. {doc.page_content[:100]}...")

if __name__ == "__main__":
    test_chatbot()