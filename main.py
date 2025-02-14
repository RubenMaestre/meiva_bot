from responder import responder_cliente

def chat():
    print("🤖 Chatbot de MEIVA SHOES - Escribe 'salir' para terminar.")
    
    # Mensaje de bienvenida más natural
    print("🤖 Bot: ¡Hola! Soy Marta. Bienvenido a Meiva Shoes. ¿En qué puedo ayudarte hoy?")
    
    chat_history = []

    while True:
        pregunta = input("👤 Tú: ")
        if pregunta.lower() == "salir":
            print("👋 ¡Hasta luego!")
            break

        respuesta = responder_cliente(pregunta, chat_history)
        chat_history.append((pregunta, respuesta))

        print(f"🤖 Bot: {respuesta}")


if __name__ == "__main__":
    chat()
