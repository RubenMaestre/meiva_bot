import streamlit as st
import openai

# Configuración de la API de OpenAI usando st.secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Chat con el Bot de Meiva Shoes")

# Entrada de usuario
user_input = st.text_input("Escribe tu pregunta:")

if st.button("Enviar"):
    if user_input:
        response = openai.Completion.create(
            model=st.secrets["FINE_TUNING_MODEL_ID"],  # Usar el ID del modelo desde secrets
            prompt=user_input,
            max_tokens=100
        )
        st.text_area("Respuesta del Bot:", response.choices[0].text.strip())
    else:
        st.warning("Por favor, escribe algo para enviar.")
