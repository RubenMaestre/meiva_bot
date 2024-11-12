import streamlit as st
from openai import OpenAI

# Configuración de la API de OpenAI usando st.secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Chat con el Bot de Meiva Shoes")

# Estado para mantener el historial de la conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Crear un contenedor para el historial del chat que ocupa 9/10 de la pantalla
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**Tú:** {msg['content']}")
        else:
            st.markdown(f"**Meiva Bot:** {msg['content']}")

# Crear un contenedor fijo en la parte inferior para la entrada y el botón de envío (1/10 de la pantalla)
st.markdown(
    """
    <style>
    .fixed-bottom-container {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: white;
        padding: 10px;
        box-shadow: 0px -2px 5px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Contenedor fijo para la entrada
st.markdown('<div class="fixed-bottom-container">', unsafe_allow_html=True)
col1, col2 = st.columns([10, 2])  # Proporción 10:2 para el campo de entrada y el botón

# Entrada de usuario
with col1:
    user_input = st.text_input("Escribe tu pregunta:", key="user_input", label_visibility="collapsed")

# Botón de envío
with col2:
    if st.button("Enviar"):
        if user_input:
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
st.markdown('</div>', unsafe_allow_html=True)
