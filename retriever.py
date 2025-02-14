from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from data_loader import cargar_preguntas_respuestas
from config import VECTOR_DB_PATH
import os

def crear_o_cargar_vectorstore():
    datos = cargar_preguntas_respuestas()
    
    # Crear documentos con contenido y metadata
    documentos = [Document(page_content=qa[0], metadata={"respuesta": qa[1]}) for qa in datos]

    # Crear o cargar FAISS
    if os.path.exists(VECTOR_DB_PATH):
        vectorstore = FAISS.load_local(VECTOR_DB_PATH, allow_dangerous_deserialization=True)
    else:
        vectorstore = FAISS.from_documents(documentos)
        vectorstore.save_local(VECTOR_DB_PATH)

    return vectorstore

# Instancia del vectorstore
vectorstore = crear_o_cargar_vectorstore()

# Convertir el vectorstore en un retriever válido
retriever = vectorstore.as_retriever()
