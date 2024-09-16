import numpy as np  

# Definición de las funciones para el perceptrón
def SIGN(WT, n, My, Mx):
    MxT = Mx[n]
    Z = np.sign(np.dot(WT, MxT))  # Usar np.dot para el producto escalar
    return Z

def omega(WT, Z, n, My, Mx):
    MxT = Mx[n]
    MyT = My[n]
    W1 = WT + (1/2) * (MyT - Z) * MxT
    return W1

# Inicialización de pesos (inicialmente asignados a 1)
W = np.array([[1], [1], [1]])
Mx = np.array([[5, 8, 1],   # Ruta 1: 5 km, 8 semáforos, tráfico bajo (-1)
               [3, 5, -1],  # Ruta 2: 3 km, 5 semáforos, tráfico bajo (-1)
               [8, 12, 1],  # Ruta 3: 8 km, 12 semáforos, tráfico alto (1)
               [6, 7, -1]]) # Ruta 4: 6 km, 7 semáforos, tráfico bajo (-1)

My = np.array([[-1],  # Ruta 1 es mala (-1)
               [-1],  # Ruta 2 es buena (-1)
               [1],   # Ruta 3 es mala (1)
               [-1]]) # Ruta 4 es buena (-1)

WT = np.transpose(W)

# Proceso de entrenamiento
Z = SIGN(WT, 0, My, Mx)
W1 = omega(WT, Z, 0, My, Mx)

Z1 = SIGN(W1, 1, My, Mx)
W2 = omega(W1, Z1, 1, My, Mx)

Z2 = SIGN(W2, 2, My, Mx)
W3 = omega(W2, Z2, 2, My, Mx)

Z3 = SIGN(W3, 3, My, Mx)
W4 = omega(W3, Z3, 3, My, Mx)

print("Pesos actualizados tras el entrenamiento:", W4)