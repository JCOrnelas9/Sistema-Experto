# Base de conocimientos: reglas que relacionan síntomas con diagnósticos
reglas = [
    {"sintomas": ["fiebre", "tos", "dolor de garganta"], "diagnostico": "gripe"},
    {"sintomas": ["dolor de cabeza", "fiebre", "nauseas"], "diagnostico": "migraña"},
    {"sintomas": ["congestión nasal", "estornudos", "picazón en los ojos"], "diagnostico": "alergia"},
]
def preguntar_sintoma(sintoma):
    respuesta = input(f"¿Tienes {sintoma}? (si/no): ").strip().lower()
    return respuesta == "si"

def inferir_diagnostico():
    sintomas_usuario = []
    
    # Recorrer todos los síntomas de la base de conocimientos
    for regla in reglas:
        sintomas_regla = regla["sintomas"]
        coincidencias = 0
        
        # Preguntar al usuario sobre cada síntoma en la regla
        for sintoma in sintomas_regla:
            if preguntar_sintoma(sintoma):
                coincidencias += 1
        
        # Si todos los síntomas coinciden, hacemos un diagnóstico
        if coincidencias == len(sintomas_regla):
            return regla["diagnostico"]
    
    return "No se pudo determinar un diagnóstico con los síntomas proporcionados."

# Ejecutar el motor de inferencia
diagnostico = inferir_diagnostico()
print(f"Diagnóstico: {diagnostico}")
