# Base de conocimiento inicial
Base_Conocimiento = {
    "hola":"Hola", "como estas?":"Bien y tu?", "de que te gustaria hablar?":"cualquier tema que te parezca interesante"
}

def Nuevo_Conocimiento(Q, A):
    """Agrega una nueva pregunta y respuesta a la base de conocimiento."""
    Base_Conocimiento[Q.lower()] = A
    print(f"Nuevo conocimiento adquirido: '{Q}' -> '{A}'")

def obtener_respuesta(Q):
    """Busca una respuesta en la base de conocimiento."""
    Q = Q.lower()
    if Q in Base_Conocimiento:
        return Base_Conocimiento[Q]
    else:
        print("Lo siento, no tengo una respuesta para esa pregunta.")
        Nueva_A = input(f"¿Cuál sería la respuesta adecuada para '{Q}'? ")
        if(Q == ""):
            print("Lo siento esa no es una respuesta, intentalo Otra vez")
        else:
            Nuevo_Conocimiento(Q, Nueva_A)
            return Nueva_A

def iniciar_chat():
    print("¡Bienvenido al chat!")
    while True:
        Q = input("\nTú: ")
        if(Q == ""):
                 print("Lo siento, ese no es un dato valido, intentalo otra vez!")
                 iniciar_chat()
        else:
           if Q.lower() == "salir":
            print("¡Hasta luego!")
            break
        A = obtener_respuesta(Q)
        print(f"Bot: {A}")
        
iniciar_chat()