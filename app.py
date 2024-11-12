import streamlit as st
import openai

# Configuración de la API de OpenAI usando st.secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Chat con el Bot de Meiva Shoes")

# Entrada de usuario
user_input = st.text_input("Escribe tu pregunta:")

if st.button("Enviar"):
    if user_input:
        try:
            response = openai.ChatCompletion.create(
                model=st.secrets["FINE_TUNING_MODEL_ID"],  # Asegúrate de que tu modelo sea compatible
                messages=[
                    {"role": "user", "content": user_input}
                ],
                max_tokens=100
            )
            st.text_area("Respuesta del Bot:", response.choices[0]["message"]["content"].strip())
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
    else:
        st.warning("Por favor, escribe algo para enviar.")
