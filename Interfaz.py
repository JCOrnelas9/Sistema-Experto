import tkinter as tk
from tkinter import messagebox

class BaseHechos:
    def __init__(self):
        self.hechos = []
    
    def agregar_hecho(self, hecho):
        if hecho not in self.hechos:
            self.hechos.append(hecho)
    
    def obtener_hechos(self):
        return self.hechos

class BaseConocimientos:
    def __init__(self):
        self.reglas = []
    
    def agregar_regla(self, sintomas, diagnostico, explicacion):
        regla = {
            "sintomas": sintomas,
            "diagnostico": diagnostico,
            "explicacion": explicacion
        }
        self.reglas.append(regla)
    
    def obtener_reglas(self):
        return self.reglas
    
    def mostrar_conocimiento(self):
        conocimiento = ""
        if not self.reglas:
            conocimiento = "La base de conocimientos está vacía."
        else:
            for i, regla in enumerate(self.reglas):
                conocimiento += f"Regla {i+1}:\n"
                conocimiento += f"  Diagnóstico: {regla['diagnostico']}\n"
                conocimiento += f"  Síntomas: {', '.join(regla['sintomas'])}\n"
                conocimiento += f"  Explicación: {regla['explicacion']}\n\n"
        return conocimiento

def inferir_diagnostico(base_conocimientos, base_hechos):
    reglas = base_conocimientos.obtener_reglas()
    hechos_usuario = base_hechos.obtener_hechos()
    
    for regla in reglas:
        sintomas_regla = regla["sintomas"]
        
        if all(sintoma in hechos_usuario for sintoma in sintomas_regla):
            return regla["diagnostico"], regla["explicacion"]
    
    return "No se pudo determinar un diagnóstico con los síntomas proporcionados.", "No se encontró una explicación."

class SistemaExpertoGUI:
    def __init__(self, root, base_conocimientos, base_hechos):
        self.root = root
        self.root.title("Sistema Experto de Diagnóstico Médico")
        
        self.base_conocimientos = base_conocimientos
        self.base_hechos = base_hechos
        
        # Título
        self.titulo = tk.Label(root, text="Sistema Experto de Diagnóstico Médico", font=("Helvetica", 16))
        self.titulo.pack(pady=10)
        
        # Botones de Modo
        self.btn_diagnostico = tk.Button(root, text="Modo Diagnóstico", command=self.modo_diagnostico)
        self.btn_diagnostico.pack(pady=5)
        
        self.btn_conocimiento = tk.Button(root, text="Modo Conocimiento", command=self.modo_conocimiento)
        self.btn_conocimiento.pack(pady=5)
        
        self.btn_salir = tk.Button(root, text="Salir", command=root.quit)
        self.btn_salir.pack(pady=5)
        
        # Area de Diagnóstico y Conocimiento
        self.text_area = tk.Text(root, height=15, width=50)
        self.text_area.pack(pady=10)
    
    def modo_diagnostico(self):
        self.text_area.delete(1.0, tk.END)
        self.base_hechos = BaseHechos()  # Reiniciar la base de hechos
        
        for regla in self.base_conocimientos.obtener_reglas():
            for sintoma in regla["sintomas"]:
                respuesta = messagebox.askquestion("Síntoma", f"¿Tienes {sintoma}?")
                if respuesta == "yes":
                    self.base_hechos.agregar_hecho(sintoma)
        
        diagnostico, explicacion = inferir_diagnostico(self.base_conocimientos, self.base_hechos)
        self.text_area.insert(tk.END, f"Diagnóstico: {diagnostico}\nExplicación: {explicacion}")
    
    def modo_conocimiento(self):
        self.text_area.delete(1.0, tk.END)
        conocimiento = self.base_conocimientos.mostrar_conocimiento()
        self.text_area.insert(tk.END, conocimiento)

# Crear la ventana principal
root = tk.Tk()

# Crear la base de conocimientos
base_conocimientos = BaseConocimientos()

# Crear la base de hechos
base_hechos = BaseHechos()

# Agregar algunas reglas a la base de conocimientos
base_conocimientos.agregar_regla(
    ["fiebre", "tos", "dolor de garganta"],
    "gripe",
    "La gripe se diagnostica cuando se presentan fiebre, tos y dolor de garganta."
)

base_conocimientos.agregar_regla(
    ["dolor de cabeza", "fiebre", "nauseas"],
    "migraña",
    "La migraña se asocia típicamente con dolor de cabeza, fiebre y náuseas."
)

base_conocimientos.agregar_regla(
    ["congestión nasal", "estornudos", "picazón en los ojos"],
    "alergia",
    "La alergia se identifica con congestión nasal, estornudos y picazón en los ojos."
)

# Crear la interfaz gráfica
app = SistemaExpertoGUI(root, base_conocimientos, base_hechos)

# Iniciar el loop de la interfaz gráfica
root.mainloop()
