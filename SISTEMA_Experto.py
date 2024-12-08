import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os
from fuzzywuzzy import fuzz

# Funciones para cargar y guardar datos
def cargar_datos(nombre_archivo):
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            try:
                return json.load(archivo)
            except json.JSONDecodeError:
                messagebox.showerror("Error", f"El archivo {nombre_archivo} no tiene un formato JSON válido.")
                return {}
    else:
        return {}

def guardar_datos(nombre_archivo, datos):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
    messagebox.showinfo("Guardado", f"Datos guardados en {nombre_archivo}.")

# Variables globales
respuestas_usuario = {}

# Cargar datos de los archivos
enfermedades = cargar_datos("enfermedades_actualizadas.json")
especies = cargar_datos("peces_actualizados.json")

# Normalización de síntomas con un diccionario de sinónimos
sinonimos = {
    "puntos blancos": ["manchas blancas", "puntos en el cuerpo"],
    "letargo": ["muy quieto", "sin moverse"],
    "respiración rápida": ["jadeo", "respiración acelerada"],
    "aletas deshilachadas": ["aletas dañadas", "aletas rasgadas"],
    "descolorido": ["sin color", "pérdida de color"],
}

def normalizar_sintoma(sintoma):
    for clave, sinonimos_lista in sinonimos.items():
        if any(sinonimo in sintoma.lower() for sinonimo in sinonimos_lista):
            return clave
    return sintoma.lower()

# Generar dinámicamente las preguntas de diagnóstico
def generar_preguntas():
    if not isinstance(enfermedades, dict):
        messagebox.showerror("Error", "El formato de enfermedades no es válido.")
        return {}

    sintomas = set()
    for enfermedad, detalles in enfermedades.items():
        if isinstance(detalles, dict) and "sintomas" in detalles:
            for sintoma in detalles["sintomas"]:
                sintomas.add(sintoma)

    preguntas = {}
    for sintoma in sintomas:
        preguntas[f"¿El pez presenta {sintoma.lower()}?"] = ["No", "Sí"]
    return preguntas

# Actualizar preguntas dinámicamente
def actualizar_preguntas_diagnostico():
    global preguntas_diagnostico
    preguntas_diagnostico = generar_preguntas()

# Inicializar preguntas de diagnóstico
preguntas_diagnostico = generar_preguntas()

# Diagnóstico de enfermedades
def iniciar_diagnostico():
    respuestas_usuario.clear()
    for widget in frame_diagnostico.winfo_children():
        widget.destroy()

    ttk.Label(frame_diagnostico, text="Selecciona los síntomas observados en tu pez:").pack(pady=10)

    for pregunta, opciones in preguntas_diagnostico.items():
        frame_pregunta = ttk.Frame(frame_diagnostico)
        frame_pregunta.pack(fill="x", pady=5)
        ttk.Label(frame_pregunta, text=pregunta).pack(side="left", padx=5)

        respuesta_var = tk.StringVar(value="No")
        respuestas_usuario[pregunta] = respuesta_var

        combo_respuesta = ttk.Combobox(frame_pregunta, textvariable=respuesta_var, values=opciones, state="readonly")
        combo_respuesta.pack(side="right", padx=5)

    ttk.Button(frame_diagnostico, text="Diagnosticar", command=diagnosticar_enfermedades).pack(pady=20)

def diagnosticar_enfermedades():
    sintomas_seleccionados = [pregunta.split("¿El pez presenta ")[1][:-1] for pregunta, respuesta in respuestas_usuario.items() if respuesta.get() == "Sí"]

    if not sintomas_seleccionados:
        messagebox.showinfo("Diagnóstico", "No seleccionaste síntomas significativos.")
        return

    sintomas_normalizados = [normalizar_sintoma(sintoma) for sintoma in sintomas_seleccionados]

    posibles_enfermedades = []
    for enfermedad, detalles in enfermedades.items():
        if isinstance(detalles, dict) and "sintomas" in detalles:
            sintomas_enfermedad = [normalizar_sintoma(sintoma) for sintoma in detalles["sintomas"]]
            coincidencias = sum(1 for sintoma_usuario in sintomas_normalizados if sintoma_usuario in sintomas_enfermedad)
            porcentaje = (coincidencias / len(sintomas_enfermedad)) * 100 if sintomas_enfermedad else 0

            if porcentaje >= 50:
                posibles_enfermedades.append(
                    f"{enfermedad} ({porcentaje:.2f}% de coincidencia):\n"
                    f"- Tratamiento: {detalles['tratamiento']}\n"
                    f"- Causa: {detalles['causa']}\n"
                    f"- Prevención: {detalles['prevencion']}\n"
                    f"- Contagioso: {'Sí' if detalles['contagioso'] else 'No'}\n"
                    f"- Duración: {detalles['duracion']}\n"
                )

    if posibles_enfermedades:
        resultado = "Posibles enfermedades y tratamientos:\n\n" + "\n\n".join(posibles_enfermedades)
        messagebox.showinfo("Diagnóstico", resultado)
    else:
        messagebox.showinfo("Diagnóstico", "No se encontraron coincidencias significativas. Consulta a un especialista.")

# Recomendación de especies
def recomendar_especies():
    try:
        pH = float(entry_ph.get())
        temp = float(entry_temp.get())
        dureza = float(entry_dureza.get())
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos.")
        return

    compatibles = [
        especie for especie, params in especies.items()
        if params["pH"][0] <= pH <= params["pH"][1]
        and params["temp"][0] <= temp <= params["temp"][1]
        and params["dureza"][0] <= dureza <= params["dureza"][1]
    ]

    if compatibles:
        messagebox.showinfo("Recomendación", f"Especies compatibles: {', '.join(compatibles)}")
    else:
        messagebox.showinfo("Recomendación", "No hay especies compatibles con los parámetros ingresados.")

# Parámetros de peces
def consultar_parametros_peces():
    especie = combo_especies.get()
    if especie in especies:
        params = especies[especie]
        info = (
            f"Parámetros ideales para {especie}:\n"
            f"- pH: {params['pH'][0]} - {params['pH'][1]}\n"
            f"- Temperatura: {params['temp'][0]}°C - {params['temp'][1]}°C\n"
            f"- Dureza: {params['dureza'][0]} - {params['dureza'][1]} dH\n"
            f"- Tamaño mínimo del acuario: {params['tamaño_acuario']}\n"
            f"- Ejemplares recomendados: {params['ejemplares_recomendados']}\n"
        )
        messagebox.showinfo("Parámetros Ideales", info)
    else:
        messagebox.showwarning("Error", "Selecciona una especie válida.")

# Agregar enfermedades
def agregar_enfermedad():
    nombre = entry_nombre_enfermedad.get()
    sintomas = text_sintomas_enfermedad.get("1.0", tk.END).strip().split("\n")
    tratamiento = text_tratamiento_enfermedad.get("1.0", tk.END).strip()
    causa = entry_causa_enfermedad.get()
    prevencion = entry_prevencion_enfermedad.get()
    contagioso = bool(combo_contagioso_enfermedad.get() == "Sí")
    duracion = entry_duracion_enfermedad.get()

    if nombre and sintomas and tratamiento:
        enfermedades[nombre] = {
            "sintomas": sintomas,
            "tratamiento": tratamiento,
            "causa": causa,
            "prevencion": prevencion,
            "contagioso": contagioso,
            "duracion": duracion
        }
        guardar_datos("enfermedades_actualizadas.json", enfermedades)
        actualizar_preguntas_diagnostico()  # Actualizar preguntas al agregar enfermedad
        entry_nombre_enfermedad.delete(0, tk.END)
        text_sintomas_enfermedad.delete("1.0", tk.END)
        text_tratamiento_enfermedad.delete("1.0", tk.END)
        entry_causa_enfermedad.delete(0, tk.END)
        entry_prevencion_enfermedad.delete(0, tk.END)
        combo_contagioso_enfermedad.set("No")
        entry_duracion_enfermedad.delete(0, tk.END)
    else:
        messagebox.showwarning("Error", "Todos los campos son obligatorios.")

# Ventana principal
root = tk.Tk()
root.title("Sistema Experto: Peces y Enfermedades")
root.geometry("900x700")

# Pestañas
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# Diagnóstico
frame_diagnostico = ttk.Frame(notebook)
notebook.add(frame_diagnostico, text="Diagnóstico de Enfermedades")
iniciar_diagnostico()

# Parámetros de Peces
frame_parametros = ttk.Frame(notebook)
notebook.add(frame_parametros, text="Parámetros de Peces")
ttk.Label(frame_parametros, text="Selecciona una especie:").pack(pady=10)
combo_especies = ttk.Combobox(frame_parametros, values=list(especies.keys()), state="readonly")
combo_especies.pack(pady=10)
ttk.Button(frame_parametros, text="Consultar Parámetros", command=consultar_parametros_peces).pack(pady=20)

# Recomendación de Especies
frame_recomendacion = ttk.Frame(notebook)
notebook.add(frame_recomendacion, text="Recomendación de Especies")
ttk.Label(frame_recomendacion, text="Introduce los parámetros del agua:").pack(pady=10)
ttk.Label(frame_recomendacion, text="pH:").pack()
entry_ph = ttk.Entry(frame_recomendacion, width=10)
entry_ph.pack(pady=5)
ttk.Label(frame_recomendacion, text="Temperatura (°C):").pack()
entry_temp = ttk.Entry(frame_recomendacion, width=10)
entry_temp.pack(pady=5)
ttk.Label(frame_recomendacion, text="Dureza (dH):").pack()
entry_dureza = ttk.Entry(frame_recomendacion, width=10)
entry_dureza.pack(pady=5)
ttk.Button(frame_recomendacion, text="Recomendar Especies", command=recomendar_especies).pack(pady=20)

# Agregar Enfermedades
frame_agregar_enfermedades = ttk.Frame(notebook)
notebook.add(frame_agregar_enfermedades, text="Agregar Enfermedades")
ttk.Label(frame_agregar_enfermedades, text="Nombre de la Enfermedad:").pack(pady=5)
entry_nombre_enfermedad = ttk.Entry(frame_agregar_enfermedades, width=50)
entry_nombre_enfermedad.pack(pady=5)
ttk.Label(frame_agregar_enfermedades, text="Síntomas (uno por línea):").pack(pady=5)
text_sintomas_enfermedad = tk.Text(frame_agregar_enfermedades, height=5, width=50)
text_sintomas_enfermedad.pack(pady=5)
ttk.Label(frame_agregar_enfermedades, text="Tratamiento:").pack(pady=5)
text_tratamiento_enfermedad = tk.Text(frame_agregar_enfermedades, height=5, width=50)
text_tratamiento_enfermedad.pack(pady=5)
ttk.Label(frame_agregar_enfermedades, text="Causa:").pack(pady=5)
entry_causa_enfermedad = ttk.Entry(frame_agregar_enfermedades, width=50)
entry_causa_enfermedad.pack(pady=5)
ttk.Label(frame_agregar_enfermedades, text="Prevención:").pack(pady=5)
entry_prevencion_enfermedad = ttk.Entry(frame_agregar_enfermedades, width=50)
entry_prevencion_enfermedad.pack(pady=5)
ttk.Label(frame_agregar_enfermedades, text="Contagioso:").pack(pady=5)
combo_contagioso_enfermedad = ttk.Combobox(frame_agregar_enfermedades, values=["No", "Sí"], state="readonly")
combo_contagioso_enfermedad.set("No")
combo_contagioso_enfermedad.pack(pady=5)
ttk.Label(frame_agregar_enfermedades, text="Duración:").pack(pady=5)
entry_duracion_enfermedad = ttk.Entry(frame_agregar_enfermedades, width=50)
entry_duracion_enfermedad.pack(pady=5)
ttk.Button(frame_agregar_enfermedades, text="Agregar Enfermedad", command=agregar_enfermedad).pack(pady=20)

# Ejecutar aplicación
root.mainloop()
