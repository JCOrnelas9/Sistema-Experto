
import pandas as pd

V = list('abcdefgh')

grafo = pd.DataFrame(index=V,columns=V)
grafo.loc['a',['b','c','g']] = 1
grafo.loc['b',['a','d','g']] = 1
grafo.loc['c',['a','d','e']] = 1
grafo.loc['d',['b','c','f']] = 1
grafo.loc['e',['c','f','g']] = 1
grafo.loc['f',['d','e','h']] = 1
grafo.loc['g',['a','b','e']] = 1
grafo.loc['h',['f']] = 1

grafo = grafo.fillna(0)
grafo.to_json("grafo.json", orient = "split")
grafo.to_json("grafo.json")

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
