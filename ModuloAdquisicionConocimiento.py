
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
        if not self.reglas:
            print("La base de conocimientos está vacía.")
        else:
            for i, regla in enumerate(self.reglas):
                print(f"Regla {i+1}:")
                print(f"  Diagnóstico: {regla['diagnostico']}")
                print(f"  Síntomas: {', '.join(regla['sintomas'])}")
                print(f"  Explicación: {regla['explicacion']}\n")

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
        
        if all(sintoma in hechos_usuario for sintoma in sintomas_regla):
            return regla["diagnostico"], regla["explicacion"]
    
    return "No se pudo determinar un diagnóstico con los síntomas proporcionados.", "No se encontró una explicación."

def modo_conocimiento(base_conocimientos):
    print("\n--- Modo de Conocimiento ---")
    base_conocimientos.mostrar_conocimiento()

def modo_diagnostico(base_conocimientos, base_hechos):
    print("\n--- Modo de Diagnóstico ---")
    
    for regla in base_conocimientos.obtener_reglas():
        for sintoma in regla["sintomas"]:
            preguntar_sintoma(sintoma, base_hechos)

    diagnostico, explicacion = inferir_diagnostico(base_conocimientos, base_hechos)
    print(f"Diagnóstico: {diagnostico}")
    print(f"Explicación: {explicacion}")

def ejecutar_sistema():
    while True:
        print("\nSeleccione un modo:")
        print("1. Modo Diagnóstico")
        print("2. Modo Conocimiento")
        print("3. Salir")
        opcion = input("Ingrese el número de su opción: ").strip()
        
        if opcion == "1":
            modo_diagnostico(base_conocimientos, base_hechos)
        elif opcion == "2":
            modo_conocimiento(base_conocimientos)
        elif opcion == "3":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

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

# Ejecutar el sistema experto
ejecutar_sistema()
