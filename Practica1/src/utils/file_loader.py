import os
from typing import List
from pypdf import PdfReader

def load_pdfs_from_folder(folder_path: str) -> List[str]:
    """
    Carga todos los PDFs de una carpeta y extrae su texto.
    
    Args:
        folder_path (str): Ruta a la carpeta con PDFs
        
    Returns:
        List[str]: Lista con el texto de todos los PDFs
    """
    documents = []
    
    # Verificar si la carpeta existe
    if not os.path.exists(folder_path):
        print(f"❌ La carpeta {folder_path} no existe")
        return documents
    
    # Buscar todos los archivos PDF en la carpeta
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("❌ No se encontraron archivos PDF en la carpeta")
        return documents
    
    print(f"📖 Encontré {len(pdf_files)} archivos PDF. Cargando...")
    
    # Leer cada PDF
    for pdf_file in pdf_files:
        try:
            file_path = os.path.join(folder_path, pdf_file)
            print(f"   Leyendo: {pdf_file}")
            
            # Extraer texto del PDF
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            documents.append(text)
            print(f"   ✅ {pdf_file} - {len(text)} caracteres extraídos")
            
        except Exception as e:
            print(f"   ❌ Error leyendo {pdf_file}: {e}")
    
    print(f"✅ Total de documentos cargados: {len(documents)}")
    return documents

# Prueba rápida para verificar que funciona
if __name__ == "__main__":
    # Probamos cargar PDFs de la carpeta data/raw
    textos = load_pdfs_from_folder("../data/raw")
    if textos:
        print(f"\n📄 Primeros 200 caracteres del primer documento:")
        print(textos[0][:200] + "...")