import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# Cargar variables de entorno (API Key)
load_dotenv()

def create_knowledge_base(pdf_folder_path: str, persist_directory: str = "./chroma_db"):
    """
    Crea una base de conocimiento vectorial a partir de PDFs
    
    Args:
        pdf_folder_path (str): Ruta a la carpeta con PDFs
        persist_directory (str): Donde guardar la base de datos
    """
    
    # 1. Cargar documentos
    from .file_loader import load_pdfs_from_folder
    documents = load_pdfs_from_folder(pdf_folder_path)
    
    if not documents:
        print("❌ No hay documentos para procesar")
        return None
    
    # 2. Dividir texto en chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    chunks = []
    for i, doc in enumerate(documents):
        doc_chunks = text_splitter.split_text(doc)
        chunks.extend(doc_chunks)
        print(f"📄 Documento {i+1} dividido en {len(doc_chunks)} chunks")
    
    print(f"✅ Total de chunks creados: {len(chunks)}")
    
    # 3. Crear embeddings y base de datos vectorial
    try:
        embeddings = OpenAIEmbeddings(
            model="text-embedding-ada-002",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Crear vector store
        vector_store = Chroma.from_texts(
            texts=chunks,
            embedding=embeddings,
            persist_directory=persist_directory
        )
        
        vector_store.persist()
        print(f"🎉 Base de conocimiento creada en: {persist_directory}")
        print(f"📊 Total de vectores almacenados: {vector_store._collection.count()}")
        
        return vector_store
        
    except Exception as e:
        print(f"❌ Error creando embeddings: {e}")
        return None

if __name__ == "__main__":
    # Ruta a la carpeta con PDFs
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "../../data/raw")
    
    # Crear base de conocimiento
    kb = create_knowledge_base(data_path)
    
    if kb:
        print("\n✅ ¡Base de conocimiento creada exitosamente!")
        print("💡 Ahora puedes usar el motor de búsqueda semántica")
    else:
        print("\n❌ No se pudo crear la base de conocimiento")