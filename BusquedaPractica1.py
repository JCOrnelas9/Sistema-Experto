
import pandas as pd
pd.set_option("future.no_silent_downcasting", True)

class Grafo:
    def _init_(self):
        self.grafo = {}

        def agregar_arista(self, nodo1, nodo2):
            if nodo1 not in self.grafo:
                self.grafo[nodo1] = []
            self.grafo[nodo1].append(nodo2)

            if nodo2 not in self.grafo:
                self.grafo[nodo2] = []
            self.grafo[nodo2].append(nodo1)

        def bfs(self, inicio, objetivo):
            visitado = set()
            cola = [[inicio]]

            if inicio == objetivo:
                return [inicio]

            while cola:
                camino = cola.pop(0)
                nodo = camino[-1]

                if nodo not in visitado:
                    for vecino in self.grafo.get(nodo, []):
                        nuevo_camino = list(camino)
                        nuevo_camino.append(vecino)
                        cola.append(nuevo_camino)

                        if vecino == objetivo:
                            return nuevo_camino
                    visitado.add(nodo)

            return None
        grafo = Grafo()
        
        inicio = 'Casa'
        objetivo = 'Ceti'
        camino = grafo.bfs(inicio, objetivo)     
        

V = list('abcdefgh')

grafo = pd.DataFrame(index=V,columns=V)
#grafo.loc['a', ['b', 'c', 'g']] = 1 a= casa
grafo.loc['a', ['b']] = 665.
grafo.loc['a', ['c']] = 926.8
grafo.loc['a', ['g']] = 1042.9

#grafo.loc['b', ['a', 'd', 'g']] = 1 b=linea2
grafo.loc['b', ['d']] = 5197.7
grafo.loc['b', ['g']] = 4397.1

#grafo.loc['c', ['a', 'd', 'e']] = 1 c=622
grafo.loc['c', ['e']] = 8227.2

#grafo.loc['d',['b','c','f']] = 1 d=Patria
grafo.loc['d', ['h']] = 1750  
#grafo.loc['d', ['f']] = 12

#grafo.loc['e',['c','f','g']] = 1 e=montevideo
grafo.loc['e', ['h']] = 320.9

#grafo.loc['f', ['d', 'e', 'h']] = 1 f= ruta 43
grafo.loc['f', ['e']] = 3941.6

#grafo.loc['g', ['a', 'b', 'e']] = 1 g=linea3
grafo.loc['g', ['d']] = 9623.3

#                                   h=ceti



#grafo = grafo.fillna(0)
#grafo.to_json("grafo.json", orient = "split")
#grafo.to_json("grafo.json")




V1 = 'h'
S = [V1]
Vp = [V1]
Ep = []
s = []
d = V.copy()
d.remove(V1)

while True:
    for x in S:

        V = [y for y in d if y in grafo.loc[grafo[x]>0,x]]
        _ = [(Ep.append((x,y)),Vp.append(y),d.remove(y),s.append(y)) for y in V]
    
    if s ==[]:      
         break
    S = s.copy()
    s = []

print(grafo)
                                                           
