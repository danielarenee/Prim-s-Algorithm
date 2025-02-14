import numpy as np  # para generar los puntos aleatorios
import matplotlib.pyplot as plt # para graficar
from scipy.spatial.distance import pdist # para obtener las aristas
from itertools import combinations # para conseguir todas las combinaciones de aristas al crear el grafo completo 

# 1) Generar los puntos aleatorios
n_points = 10
points = np.random.uniform(0, 100, size=(n_points, 2))  # n puntos con 2 coordinadas (plano 2D), matriz de tamaño 
print("Puntos generados:\n", points)

# 2) Calcular las aristas con sus pesos usando pdist y combinations
edge_weights = pdist(points)  # calcula las distancias entre cada par de nodos
edges = list(combinations(range(n_points), 2))  # genera todas las combinaciones posibles de nodos
weighted_edges = list(zip(edges, edge_weights))  # asigna pesos a las aristas con list y zip
# Ordenar las aristas por peso antes de usar Prim
weighted_edges.sort(key=lambda x: x[1])  # ordena por el peso (segundo valor en la tupla)

# 3) Función para graficar con matplotlib
def plot_graph(edges, points, title="Graph", filename=None, show=True):
    plt.figure(figsize=(8, 8)) #tamaño de la figura

    # nodos 
    x, y = points[:, 0], points[:, 1]  # extrae las coordenadas x y y de la matriz de puntos
    plt.scatter(x, y, color="pink", zorder=2, s=100)  # dibuja los nodos rositas
    for i, (x_coord, y_coord) in enumerate(points): #recorre los nodos y los etiqueta
        plt.text(x_coord, y_coord, f"{i}", fontsize=12, color="purple", zorder=3) # escribe el indice sobre el nodo

    # aristas
    for edge in edges:  # Dibujamos las aristas seleccionadas
        u, v = edge
        plt.plot([points[u, 0], points[v, 0]],
                 [points[u, 1], points[v, 1]],
                 color="gray", linestyle="--", zorder=1)

    plt.title(title) # agrega el titulo de la grafica 
    if filename:
        plt.savefig(filename) #si el filename no es none, guarda la imagen con filename
    if show:
        plt.show()
    plt.close()

# 4) Graficar el grafo completo
plot_graph([edge for edge, _ in weighted_edges], points, title="Complete Graph", filename="complete_graph.png") #ignorando el peso

# 5) Algoritmo de Prim - - - - - - - - - - - - - - - - - -

visited = set()  # conjunto de nodos visitados
unvisited = set(range(n_points)) # conjunto de nodos no visitados , inicialmente todos estan aqui 

# nodo inicial arbitrario
start_node = 0
visited.add(start_node) # se marca como visitado
unvisited.remove(start_node)  # Se elimina el nodo inicial de los no visitados

mst_edges = [] 

while unvisited: # mientras haya nodos no visitados
    min_edge = None
    min_weight = float('inf')
    
    # recorre todas las aristas y sus pesos
    for (u, v), weight in weighted_edges:

    # verifica si esta arista conecta un nodo visitado con uno no visitado
        if (u in visited and v in unvisited) or (v in visited and u in unvisited):  
        # si el peso de esta arista es menor que el mínimo encontrado hasta ahora
            if weight < min_weight:
                min_edge = (u, v)  # actualiza la mejor arista 
                min_weight = weight  # actualiza el peso minimo

     # añadir la arista mínima al MST
    if min_edge:
        mst_edges.append(min_edge)
        visited.add(min_edge[1]) if min_edge[0] in visited else visited.add(min_edge[0])
        unvisited.remove(min_edge[1]) if min_edge[1] in unvisited else unvisited.remove(min_edge[0])

# 6) Graficar el MST
print("\n -- Árbol de Cobertura Mínima (MST) -- ")
print(mst_edges)
plot_graph(mst_edges, points, title="Minimum Spanning Tree (MST)", filename="mst.png")
