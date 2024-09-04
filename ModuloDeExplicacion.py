
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

    # Crear una instancia de la base de conocimientos
base_conocimientos = BaseConocimientos()

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
def preguntar_sintoma(sintoma):
    respuesta = input(f"¿Tienes {sintoma}? (si/no): ").strip().lower()
    return respuesta == "si"
def inferir_diagnostico(base_conocimientos):
    reglas = base_conocimientos.obtener_reglas()
    
    for regla in reglas:
        sintomas_regla = regla["sintomas"]
        coincidencias = 0
        
        for sintoma in sintomas_regla:
            if preguntar_sintoma(sintoma):
                coincidencias += 1
        
        if coincidencias == len(sintomas_regla):
            return regla["diagnostico"], regla["explicacion"]
    
    return "No se pudo determinar un diagnóstico con los síntomas proporcionados.", "No se encontró una explicación."

# Ejecutar el motor de inferencia
diagnostico, explicacion = inferir_diagnostico(base_conocimientos)
print(f"Diagnóstico: {diagnostico}")
print(f"Explicación: {explicacion}")

    
