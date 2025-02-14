from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from retriever import retriever
from config import OLLAMA_MODEL

# Instancia del modelo Ollama
llm = Ollama(model=OLLAMA_MODEL)

# Configurar memoria para recordar contexto
memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")

# Lista de saludos comunes para detectar una bienvenida
SALUDOS = ["hola", "buenos días", "buenas tardes", "buenas noches", "qué tal", "cómo estás", "puedes ayudarme"]

def responder_cliente(pregunta, chat_history=[]):
    """Responde al cliente basándose en FAISS y reformula la respuesta con Ollama."""
    
    # Convertir pregunta a minúsculas para comparación
    pregunta_lower = pregunta.lower().strip()

    # Si el usuario solo saluda, responder con una bienvenida especial
    if any(saludo in pregunta_lower for saludo in SALUDOS):
        return iter(["¡Hola! 😊 Soy Marta, tu asistente especializada de Meiva Shoes. Estoy aquí para ayudarte con cualquier consulta sobre nuestros productos, envíos o cualquier otra duda que tengas. ¿En qué puedo ayudarte hoy? 👠💬"])

    # Buscar la mejor respuesta en FAISS
    mejor_respuesta = retriever.get_relevant_documents(pregunta)

    if mejor_respuesta:
        mejor_respuesta = mejor_respuesta[0].metadata["respuesta"]
    else:
        mejor_respuesta = "No tengo información exacta sobre eso, pero puedo ayudarte con otra consulta."

    # Prompt para reformular con Ollama
    prompt = f"""
    Te llamas Marta. Actúa como un asistente experto en Meiva Shoes. Reformula esta respuesta para que sea más natural y conversacional:
    Pregunta del cliente: {pregunta}
    Respuesta encontrada: {mejor_respuesta}

    Reformula la respuesta para que sea clara, amigable y natural. Pero no inventes información.
    """

    # ⚡ Generamos la respuesta en STREAM
    return llm.stream(prompt)
