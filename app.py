import streamlit as st
from openai import OpenAI

# Configuración de la API de OpenAI usando st.secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Chat con el Bot de Meiva Shoes")

# Estado para mantener el historial de la conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Entrada de usuario
user_input = st.text_input("Escribe tu pregunta:", key="user_input")

if st.button("Enviar") and user_input:
    # Agregar la pregunta del usuario al historial
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    try:
        # Realizar la consulta al modelo
        response = client.chat.completions.create(
            model=st.secrets["FINE_TUNING_MODEL_ID"],  # Usar el ID del modelo desde secrets
            messages=st.session_state.messages,
            max_tokens=100
        )
        # Obtener la respuesta del bot
        bot_response = response.choices[0].message.content
        # Agregar la respuesta del bot al historial
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
    except Exception as e:
        st.error(f"Ocurrió un error: {e}")

# Mostrar el historial de la conversación (hacia arriba)
for msg in reversed(st.session_state.messages):  # Invertimos el orden para mostrar el historial hacia arriba
    if msg["role"] == "user":
        st.markdown(f"**Tú:** {msg['content']}")
    else:
        st.markdown(f"**Meiva Bot:** {msg['content']}")
