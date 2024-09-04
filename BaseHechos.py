
    
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

def preguntar_sintoma(sintoma, base_hechos):
    respuesta = input(f"¿Tienes {sintoma}? (si/no): ").strip().lower()
    if respuesta == "si":
        base_hechos.agregar_hecho(sintoma)
        return True
    return False

def inferir_diagnostico(base_conocimientos, base_hechos):
    reglas = base_conocimientos.obtener_reglas()
    hechos_usuario = base_hechos.obtener_hechos()
    
    for regla in reglas:
        sintomas_regla = regla["sintomas"]
        
        # Verificar si todos los síntomas de la regla están en los hechos del usuario
        if all(sintoma in hechos_usuario for sintoma in sintomas_regla):
            return regla["diagnostico"], regla["explicacion"]
    
    return "No se pudo determinar un diagnóstico con los síntomas proporcionados.", "No se encontró una explicación."

# Crear una instancia de la base de conocimientos
base_conocimientos = BaseConocimientos()

# Crear una instancia de la base de hechos
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

# Recorrer las reglas y preguntar al usuario sobre los síntomas
for regla in base_conocimientos.obtener_reglas():
    for sintoma in regla["sintomas"]:
        preguntar_sintoma(sintoma, base_hechos)

# Inferir el diagnóstico basado en la base de hechos
diagnostico, explicacion = inferir_diagnostico(base_conocimientos, base_hechos)
print(f"Diagnóstico: {diagnostico}")
print(f"Explicación: {explicacion}")
