import streamlit as st
import openai  # Asegúrate de tener la biblioteca openai instalada y configurada

# Configuración de la API de OpenAI
openai.api_key = "tu_api_key_de_openai"

st.title("Chat con tu Bot de Fine-Tuning")

# Entrada de usuario
user_input = st.text_input("Escribe tu pregunta:")

if st.button("Enviar"):
    if user_input:
        response = openai.Completion.create(
            model="tu_modelo_fine_tuning_id",  # Reemplaza con tu modelo
            prompt=user_input,
            max_tokens=100
        )
        st.text_area("Respuesta del Bot:", response.choices[0].text.strip())
    else:
        st.warning("Por favor, escribe algo para enviar.")
