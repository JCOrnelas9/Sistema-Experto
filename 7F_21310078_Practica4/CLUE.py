import tkinter as tk
from tkinter import messagebox
import random
import sys

# Datos del juego
personajes = ["Detective Ramírez", "Srta. Camila", "Dr. Lorenzo", "Capitán Morales", "Sra. Elvira"]
lugares = ["Baño", "Cocina", "Jardín", "Estudio", "Comedor"]
armas = ["Candelabro", "Daga", "Pistola", "Veneno", "Llave Inglesa"]

# Asignación de imágenes
imagenes_personajes = {
    "Detective Ramírez": "ramirez.png",
    "Srta. Camila": "camila.png",
    "Dr. Lorenzo": "lorenzo.png",
    "Capitán Morales": "morales.png",
    "Sra. Elvira": "elvira.png"
}
imagenes_lugares = {
    "Baño": "baño.png",
    "Cocina": "cocina.png",
    "Jardín": "jardin.png",
    "Estudio": "estudio.png",
    "Comedor": "comedor.png"
}
imagenes_armas = {
    "Candelabro": "candelabro.png",
    "Daga": "daga.png",
    "Pistola": "pistola.png",
    "Veneno": "veneno.png",
    "Llave Inglesa": "llave.png"
}

# Historias base
historias_base = [
    {"personaje": "Srta. Camila", "lugar": "Cocina", "arma": "Daga"},
    {"personaje": "Dr. Lorenzo", "lugar": "Jardín", "arma": "Pistola"},
    {"personaje": "Capitán Morales", "lugar": "Estudio", "arma": "Veneno"},
    {"personaje": "Sra. Elvira", "lugar": "Comedor", "arma": "Llave Inglesa"},
    {"personaje": "Detective Ramírez", "lugar": "Biblioteca", "arma": "Candelabro"}
]

# Variables del juego
interacciones = 0
ventanas_abiertas = []
historia_falsa = None

def iniciar_juego():
    """Inicia el juego seleccionando una historia falsa."""
    global interacciones, historia_falsa
    interacciones = 0
    historia_falsa = random.choice(historias_base)  # Asegurar que historia_falsa no sea None
    random.shuffle(personajes)
    random.shuffle(lugares)
    random.shuffle(armas)
    print(f"Historia falsa seleccionada: {historia_falsa}")  # Debugging para verificar la historia

def cargar_fondo(ventana):
    """Agregar imagen de fondo."""
    try:
        fondo = tk.PhotoImage(file="fondo.png")
        label_fondo = tk.Label(ventana, image=fondo)
        label_fondo.image = fondo
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Error al cargar la imagen de fondo: {e}")
        sys.exit()

def cerrar_ventanas():
    """Cierra todas las ventanas abiertas."""
    for ventana in ventanas_abiertas:
        if ventana.winfo_exists():
            ventana.destroy()
    ventanas_abiertas.clear()

def seleccionar_categoria():
    """Selecciona una categoría."""
    cerrar_ventanas()
    ventana_categoria = tk.Toplevel(ventana)
    cargar_fondo(ventana_categoria)
    ventana_categoria.title("Selecciona una Categoría")
    ventanas_abiertas.append(ventana_categoria)

    tk.Button(ventana_categoria, text="Personajes", command=lambda: seleccionar_elemento("personaje", personajes, imagenes_personajes)).pack(pady=10)
    tk.Button(ventana_categoria, text="Lugares", command=lambda: seleccionar_elemento("lugar", lugares, imagenes_lugares)).pack(pady=10)
    tk.Button(ventana_categoria, text="Armas", command=lambda: seleccionar_elemento("arma", armas, imagenes_armas)).pack(pady=10)

def seleccionar_elemento(categoria, opciones, imagenes):
    """Selecciona un elemento dentro de la categoría."""
    ventana_opciones = tk.Toplevel(ventana)
    cargar_fondo(ventana_opciones)
    ventana_opciones.title(f"Selecciona un {categoria.capitalize()}")
    ventanas_abiertas.append(ventana_opciones)

    for i, opcion in enumerate(opciones):
        frame = tk.Frame(ventana_opciones)
        frame.grid(row=i // 3, column=i % 3, padx=5, pady=5)

        try:
            img = tk.PhotoImage(file=imagenes[opcion]).subsample(5, 5)
            label = tk.Label(frame, image=img)
            label.image = img  # Guardar referencia
            label.pack()
        except Exception as e:
            print(f"Error al cargar la imagen para {opcion}: {e}")

        tk.Button(frame, text=opcion, command=lambda o=opcion: mostrar_respuesta(o, categoria)).pack()

def mostrar_respuesta(elemento, categoria):
    """Muestra la pista."""
    respuesta = generar_respuesta(elemento, categoria)
    messagebox.showinfo("Pista", respuesta)
    registrar_interaccion()

def generar_respuesta(elemento, categoria):
    """Genera la pista según la historia."""
    if historia_falsa is None:
        iniciar_juego()  # Asegura que historia_falsa no sea None

    for historia in historias_base:
        if historia[categoria] == elemento:
            if historia == historia_falsa:
                return f"{elemento}: No fue visto o no estaba.\nLugar relacionado: {historia['lugar']}.\nArma relacionada: {historia['arma']}."
            else:
                return f"{elemento}: Fue visto o estaba.\nLugar relacionado: {historia['lugar']}.\nArma relacionada: {historia['arma']}."
    return f"{elemento}: No se encontró información."

def registrar_interaccion():
    """Registra la interacción y verifica si alcanzó el límite."""
    global interacciones
    interacciones += 1
    if interacciones >= 3:
        iniciar_adivinanza()
    else:
        seleccionar_categoria()

def iniciar_adivinanza():
    """Permite hacer la hipótesis."""
    cerrar_ventanas()
    ventana_adivinanza = tk.Toplevel(ventana)
    cargar_fondo(ventana_adivinanza)
    ventana_adivinanza.title("Haz tu Hipótesis")
    ventanas_abiertas.append(ventana_adivinanza)

    tk.Label(ventana_adivinanza, text="Selecciona un personaje:").pack()
    personaje_var = tk.StringVar(ventana_adivinanza)
    personaje_var.set(personajes[0])
    tk.OptionMenu(ventana_adivinanza, personaje_var, *personajes).pack()

    tk.Label(ventana_adivinanza, text="Selecciona un lugar:").pack()
    lugar_var = tk.StringVar(ventana_adivinanza)
    lugar_var.set(lugares[0])
    tk.OptionMenu(ventana_adivinanza, lugar_var, *lugares).pack()

    tk.Label(ventana_adivinanza, text="Selecciona un arma:").pack()
    arma_var = tk.StringVar(ventana_adivinanza)
    arma_var.set(armas[0])
    tk.OptionMenu(ventana_adivinanza, arma_var, *armas).pack()

    tk.Button(ventana_adivinanza, text="Adivinar", command=lambda: verificar(personaje_var.get(), lugar_var.get(), arma_var.get())).pack(pady=10)

def verificar(personaje, lugar, arma):
    """Verifica la hipótesis."""
    if historia_falsa is None:
        iniciar_juego()  # Asegura que historia_falsa no sea None

    if (personaje == historia_falsa["personaje"] and lugar == historia_falsa["lugar"] and arma == historia_falsa["arma"]):
        messagebox.showinfo("¡Correcto!", "¡Descubriste la historia falsa!")
    else:
        mensaje = f"No acertaste. La historia falsa era:\n\nPersonaje: {historia_falsa['personaje']}, Lugar: {historia_falsa['lugar']}, Arma: {historia_falsa['arma']}."
        messagebox.showinfo("Incorrecto", mensaje)
    reiniciar_juego()

def reiniciar_juego():
    """Reinicia el juego."""
    iniciar_juego()
    seleccionar_categoria()

def finalizar_juego():
    """Finaliza el juego."""
    cerrar_ventanas()
    ventana.destroy()
    sys.exit()

ventana = tk.Tk()
ventana.title("Juego del Misterio")
cargar_fondo(ventana)

tk.Label(
    ventana, 
    text="Héctor Salinas yace en el suelo, con los ojos abiertos, como si aún "
         "intentara comprender lo que había pasado. Su respiración se apagó en "
         "un instante, y el eco de sus últimas palabras quedó atrapado en el aire. "
         "Nadie escuchó un grito. Nadie pidió ayuda. Solo el silencio envolvió la escena, "
         "tan frío como el acero.\n\nCinco personas estaban cerca en el momento de su muerte, "
         "cada una con una mirada distinta: miedo, ira, indiferencia… o tal vez todas eran "
         "máscaras bien colocadas.\n\nUno de ellos sabía la verdad. Uno lo hizo. "
         "Y ahora te toca descubrir quién fue. ¿Te atreves a desenmascarar al asesino?", 
    wraplength=500,  # Ajusta el ancho del texto
    justify="left"  # Alinea el texto a la izquierda para que se vea ordenado
).pack(padx=20, pady=20)

tk.Button(ventana, text="Comenzar", command=seleccionar_categoria).pack(pady=10)
tk.Button(ventana, text="Finalizar Juego", command=finalizar_juego).pack(pady=10)

ventana.mainloop()
