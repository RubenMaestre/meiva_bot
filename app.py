import streamlit as st
from responder import responder_cliente
import time  # Para simular el efecto de escritura progresiva

st.title("🤖 Chat con el Bot de Meiva Shoes (Ollama)")

# Estado para mantener el historial de la conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar el historial de la conversación
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    with st.chat_message(role):
        st.markdown(content)

# Entrada del usuario
user_input = st.chat_input("Escribe tu pregunta:")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        # Obtener la respuesta del bot en formato de streaming
        response_stream = responder_cliente(user_input)  

        # Contenedor para mostrar la respuesta progresivamente
        with st.chat_message("assistant"):
            response_container = st.empty()  
            full_response = ""

            for chunk in response_stream:
                full_response += chunk  # Agregar el fragmento a la respuesta completa
                response_container.markdown(full_response)  # Actualizar el texto en tiempo real
                time.sleep(0.05)  # ⚡ Ajusta este tiempo si quieres más o menos velocidad

        # Guardar la respuesta en el historial
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    except Exception as e:
        st.error(f"⚠️ Ocurrió un error: {e}")
