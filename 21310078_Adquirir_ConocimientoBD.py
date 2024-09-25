import json
import os

# Ruta del archivo JSON
archivo_base = "conocimiento.json"

# Cargar la base de conocimiento desde el archivo JSON
def cargar_base_conocimiento():
    if os.path.exists(archivo_base):
        with open(archivo_base, 'r') as archivo:
            return json.load(archivo)
    else:
        return {
            "hola": "Hola", 
            "como estas?": "Bien y tú?", 
            "de que te gustaria hablar?": "Cualquier tema que te parezca interesante"
        }

# Guardar la base de conocimiento en el archivo JSON
def guardar_base_conocimiento():
    with open(archivo_base, 'w') as archivo:
        json.dump(Base_Conocimiento, archivo, indent=4)
    print("Base de conocimiento guardada correctamente.")

# Inicializar la base de conocimiento
Base_Conocimiento = cargar_base_conocimiento()

def Nuevo_Conocimiento(Q, A):
    """Agrega una nueva pregunta y respuesta a la base de conocimiento."""
    Base_Conocimiento[Q.lower()] = A
    print(f"Nuevo conocimiento adquirido: '{Q}' -> '{A}'")
    guardar_base_conocimiento()

def obtener_respuesta(Q):
    """Busca una respuesta en la base de conocimiento."""
    Q = Q.lower()
    if Q in Base_Conocimiento:
        return Base_Conocimiento[Q]
    else:
        print("Lo siento, no tengo una respuesta para esa pregunta.")
        Nueva_A = input(f"¿Cuál sería la respuesta adecuada para '{Q}'? ")
        if Nueva_A == "":
            print("Lo siento, esa no es una respuesta válida, intentalo otra vez.")
        else:
            Nuevo_Conocimiento(Q, Nueva_A)
            return Nueva_A

def iniciar_chat():
    print("¡Bienvenido al chat!")
    while True:
        Q = input("\nTú: ")
        if Q == "":
            print("Lo siento, ese no es un dato válido, inténtalo otra vez.")
            continue
        if Q.lower() == "salir":
            print("¡Hasta luego!")
            guardar_base_conocimiento()
            break
        A = obtener_respuesta(Q)
        print(f"Bot: {A}")

# Iniciar el chat
iniciar_chat()