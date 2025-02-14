from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama  # Importamos Ollama en vez de OpenAI
from config import OLLAMA_MODEL

# Instancia del modelo local con Ollama
llm = Ollama(model=OLLAMA_MODEL)

# Agente de atención al cliente
customer_support_agent = Agent(
    name="Soporte AI",
    role="Responde preguntas de clientes basándose en la base de datos de preguntas frecuentes.",
    llm=llm,
    description="Este agente busca la mejor respuesta en la base de datos y la reformula para dar una respuesta clara y útil."
)

# Definir la tarea
task = Task(
    description="Responder consultas de clientes usando la información de la base de datos.",
    agent=customer_support_agent
)

# Crew con el agente
crew = Crew(agents=[customer_support_agent], tasks=[task])
