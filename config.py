import os
import streamlit as st

# Clave de API de OpenAI (debes configurarla como variable de entorno)
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

# Configuración de modelos
OPENAI_MODEL = "gpt-4"
EMBEDDINGS_MODEL = "text-embedding-ada-002"

# Directorios
FAQ_JSONL_PATH = "meiva_bot/data/faq.jsonl"
VECTOR_DB_PATH = "meiva_bot/models/faiss_index"
