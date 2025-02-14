from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.memory import ConversationBufferMemory  # ✅ Corrección aquí
from langchain.chains import ConversationalRetrievalChain
from retriever import retriever  # ✅ Ahora usamos el retriever correcto
from config import OPENAI_MODEL, OPENAI_API_KEY

# Configurar API Key
import os
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Instancia del modelo OpenAI
llm = ChatOpenAI(model_name=OPENAI_MODEL)

# Configurar memoria para recordar contexto
memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")

# Crear la cadena de respuesta con memoria y búsqueda en la base de datos
chat_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,  # ✅ Ahora usa el retriever correcto
    memory=memory
)

def responder_cliente(pregunta, chat_history=[]):
    mejor_respuesta = retriever.get_relevant_documents(pregunta)  # ✅ Ajustado para usar retriever correctamente

    if mejor_respuesta:
        mejor_respuesta = mejor_respuesta[0].metadata["respuesta"]
    else:
        mejor_respuesta = "No tengo información exacta sobre eso, pero puedo ayudarte con otra consulta."

    # Reformular con OpenAI para hacerlo más natural
    prompt = f"""
    Te llamas Marta. Actúa como un asistente experto en Meiva Shoes. Reformula esta respuesta para que sea más natural y conversacional:
    Pregunta del cliente: {pregunta}
    Respuesta encontrada: {mejor_respuesta}

    Reformula la respuesta para que sea clara, amigable y natural. Pero no inventes información.
    """
    respuesta_final = llm.invoke(prompt).content

    return respuesta_final
