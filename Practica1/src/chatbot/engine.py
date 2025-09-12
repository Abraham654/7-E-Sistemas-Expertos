import os
import sys
from typing import List, Dict
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from dotenv import load_dotenv

# Configurar paths
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

# Cargar variables de entorno
load_dotenv()

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
            
            # 4. Crear cadena de QA
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.get_llm(),
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
                chain_type_kwargs={"prompt": PROMPT},
                return_source_documents=True
            )
            
            print("✅ Motor del chatbot inicializado correctamente")
            
        except Exception as e:
            print(f"❌ Error inicializando el motor: {e}")
            raise
    
    def get_llm(self):
        """Obtiene el modelo de lenguaje a usar"""
        # Opción 1: Usar Ollama (si está instalado)
        try:
            return Ollama(model="llama2")
        except:
            # Opción 2: Usar un mock para pruebas
            print("⚠️  Usando simulador de LLM para pruebas. Instala Ollama para respuestas reales.")
            return self.get_mock_llm()
    
    def get_mock_llm(self):
        """Simulador de LLM para pruebas"""
        from langchain_core.language_models import BaseLLM
        from langchain_core.callbacks import CallbackManagerForLLMRun
        from langchain_core.outputs import LLMResult
        from typing import Any, List, Optional
        
        class MockLLM(BaseLLM):
            def _generate(self, prompts: List[str], stop: Optional[List[str]] = None, 
                         run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs: Any) -> LLMResult:
                responses = []
                for prompt in prompts:
                    if "aceite" in prompt.lower():
                        responses.append("El cambio de aceite se recomienda cada 5,000 km o 6 meses. Use aceite 5W-30 sintético.")
                    elif "freno" in prompt.lower():
                        responses.append("Las pastillas de freno deben revisarse cada 10,000 km y cambiarse cuando el grosor sea menor a 3mm.")
                    else:
                        responses.append("Basado en el manual de mecánica, recomiendo revisar el vehículo con un especialista.")
                
                return LLMResult(generations=[[{"text": response}] for response in responses])
            
            @property
            def _llm_type(self) -> str:
                return "mock"
        
        return MockLLM()
    
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
                "sources": result["source_documents"]
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
        "¿Qué significa el humo azul del escape?"
    ]
    
    for question in test_questions:
        print(f"\n🧑‍💼 Pregunta: {question}")
        response = chatbot.ask_question(question)
        print(f"🤖 Respuesta: {response['answer']}")
        
        if response['sources']:
            print("📚 Fuentes utilizadas:")
            for i, doc in enumerate(response['sources'][:2]):
                print(f"   {i+1}. {doc.page_content[:100]}...")

if __name__ == "__main__":
    test_chatbot()