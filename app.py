import streamlit as st
import requests

API_URL = "http://138.199.169.157:8006/chat"  # ✅ URL corregida

st.title("🛍️ Asistente Virtual de MEIVA SHOES 👠")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Escribe tu pregunta:")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Pensando... 💭")

        response = requests.post(API_URL, json={"question": user_input})

        if response.ok:
            respuesta = response.json().get("response", "Disculpa, no tengo respuesta en este momento.")
        else:
            response.raise_for_status()

        message_placeholder.markdown(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": response})