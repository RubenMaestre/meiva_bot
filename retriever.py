from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from data_loader import cargar_preguntas_respuestas
from config import VECTOR_DB_PATH, OPENAI_API_KEY

import os

# Configurar API Key
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def crear_o_cargar_vectorstore():
    datos = cargar_preguntas_respuestas()
    
    # Crear documentos con contenido y metadata
    documentos = [Document(page_content=qa[0], metadata={"respuesta": qa[1]}) for qa in datos]

    # Crear o cargar FAISS
    if os.path.exists(VECTOR_DB_PATH):
        vectorstore = FAISS.load_local(VECTOR_DB_PATH, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
    else:
        vectorstore = FAISS.from_documents(documentos, OpenAIEmbeddings())
        vectorstore.save_local(VECTOR_DB_PATH)

    return vectorstore

# Instancia del vectorstore
vectorstore = crear_o_cargar_vectorstore()

# Convertir el vectorstore en un retriever válido para LangChain
retriever = vectorstore.as_retriever()

# Función para buscar respuesta en la base de datos
def buscar_respuesta(pregunta, top_k=3):
    """Obtiene las respuestas más relevantes de la base de datos FAISS."""
    similares = retriever.get_relevant_documents(pregunta, k=top_k)  # 🛠️ Ajuste aquí

    if similares:
        respuestas = [s.metadata["respuesta"] for s in similares]
        return " ".join(respuestas[:1])  # Devuelve la respuesta más relevante
    
    return "No tengo información exacta sobre eso, pero puedo ayudarte con otra consulta."
