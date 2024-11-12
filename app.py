import streamlit as st
import openai

# Configuración de la API de OpenAI usando st.secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Chat con el Bot de Meiva Shoes")

# Estado para mantener el historial de la conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar el historial de la conversación
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# Entrada de usuario
user_input = st.chat_input("Escribe tu pregunta:")

if user_input:
    # Agregar la pregunta del usuario al historial
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    try:
        # Realizar la consulta al modelo
        response = openai.ChatCompletion.create(
            model=st.secrets["FINE_TUNING_MODEL_ID"],
            messages=st.session_state.messages,
            max_tokens=100
        )
        # Obtener la respuesta del bot
        bot_response = response.choices[0].message["content"]
        # Agregar la respuesta del bot al historial
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)
    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
