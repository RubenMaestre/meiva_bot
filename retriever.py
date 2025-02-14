import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings  # Usa embeddings de Ollama
from langchain.schema import Document
from data_loader import cargar_preguntas_respuestas
from config import VECTOR_DB_PATH

# Crear instancia de embeddings de Ollama
embeddings = OllamaEmbeddings(model="mistral")  # Puedes cambiar 'mistral' por otro modelo de Ollama

def crear_o_cargar_vectorstore():
    datos = cargar_preguntas_respuestas()

    # Crear documentos con contenido y metadata
    documentos = [Document(page_content=qa[0], metadata={"respuesta": qa[1]}) for qa in datos]

    # Verificar si la base de datos FAISS existe
    if os.path.exists(VECTOR_DB_PATH):
        try:
            vectorstore = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
        except Exception as e:
            print(f"⚠️ Error cargando FAISS: {e}. Se regenerará el índice.")
            vectorstore = FAISS.from_documents(documentos, embeddings)
            vectorstore.save_local(VECTOR_DB_PATH)
    else:
        vectorstore = FAISS.from_documents(documentos, embeddings)
        vectorstore.save_local(VECTOR_DB_PATH)

    return vectorstore

# Instancia del vectorstore
vectorstore = crear_o_cargar_vectorstore()

# Convertir el vectorstore en un retriever válido
retriever = vectorstore.as_retriever()
