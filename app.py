import streamlit as st
from openai import OpenAI

# Configuración de la API de OpenAI usando st.secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Chat con el Bot de Meiva Shoes")

# Estado para mantener el historial de la conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar el historial de la conversación en un contenedor
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**Tú:** {msg['content']}")
        else:
            st.markdown(f"**Meiva Bot:** {msg['content']}")

# Añadir un separador
st.write("---")

# Crear un contenedor en la parte inferior para la entrada de texto y el botón
input_container = st.empty()
with input_container.container():
    col1, col2 = st.columns([10, 2])  # Proporción de 10:2 para entrada y botón
    with col1:
        user_input = st.text_input("Escribe tu pregunta:", key="user_input", label_visibility="collapsed")
    with col2:
        send_button = st.button("Enviar")

# Manejar el envío de la pregunta cuando se presiona el botón
if send_button and user_input:
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
    
    # Limpiar la entrada de texto después de enviar la pregunta
    st.experimental_rerun()
