import streamlit as st
import requests

API_URL = "http://138.199.169.157:8006/chat"  # ✅ URL corregida

st.title("🛍️ Asistente Virtual de MEIVA SHOES 👠")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial de mensajes
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input del usuario
user_input = st.chat_input("¿En qué puedo ayudarte?")

if user_input := user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("...")

        # Petición a tu API FastAPI
        response = requests.post(API_URL, json={"question": user_input})

        if (response_json := response.json()).get("response"):
            response_text = response_json["response"]  # ✅ Define response_text
            message_placeholder.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        else:
            message_placeholder.markdown("⚠️ Lo siento, hubo un problema con la respuesta.")
