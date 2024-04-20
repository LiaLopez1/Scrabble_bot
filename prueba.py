from collections import deque
import heapq
import tkinter as tk
from tkinter import simpledialog, messagebox, Label, Entry, Button

class Estado:
    def __init__(self, tablero, padre=None, movimiento=None, profundidad=0, costo=0):
        self.tablero = tablero
        self.padre = padre
        self.movimiento = movimiento
        self.profundidad = profundidad
        self.costo = costo  # Este serÃ¡ utilizado para A*

    def __str__(self):
        return '\n'.join([' '.join(map(str, self.tablero[i:i+3])) for i in range(0, 9, 3)])

    def __eq__(self, otro):
        return self.tablero == otro.tablero

    def __lt__(self, otro):
        return self.costo < otro.costo

    def generar_sucesores(self):
        sucesores = []
        index_0 = self.tablero.index(0)
        row, col = divmod(index_0, 3)
        movimientos = {
            'Arriba': -3 if row > 0 else None,
            'Abajo': 3 if row < 2 else None,
            'Izquierda': -1 if col > 0 else None,
            'Derecha': 1 if col < 2 else None,
        }

        for direccion, cambio in movimientos.items():
            if cambio is not None:
                tablero_nuevo = self.tablero[:]
                index_nuevo = index_0 + cambio
                tablero_nuevo[index_0], tablero_nuevo[index_nuevo] = tablero_nuevo[index_nuevo], tablero_nuevo[index_0]
                nuevo_costo = self.costo + 1
                sucesores.append(Estado(tablero_nuevo, self, direccion, self.profundidad + 1, nuevo_costo))

        return sucesores

#resuelve el puzzle por metodo de anchura
def resolver_puzzleBFS(estado_inicial, estado_objetivo):
    if not es_solucionable(estado_inicial):
        return None
    
    frontera = deque([Estado(estado_inicial)])
    visitados = set()
    visitados.add(tuple(estado_inicial))

    while frontera:
        estado_actual = frontera.popleft()
        
        if estado_actual.tablero == estado_objetivo:
            return estado_actual
        
        for sucesor in estado_actual.generar_sucesores():
            if tuple(sucesor.tablero) not in visitados:
                visitados.add(tuple(sucesor.tablero))
                frontera.append(sucesor)

    return None


# resuelve con el metodo de profundidad
def Resolver_PuzzleDFS(estado_inicial, estado_objetivo, profundidad_max=30):
    frontera = [Estado(estado_inicial)]
    visitados = set()
    visitados.add(tuple(estado_inicial))

    while frontera:
        estado_actual = frontera.pop()  # Cambio principal respecto a BFS: pop() en lugar de popleft()

        if estado_actual.tablero == estado_objetivo:
            return estado_actual
        
        if estado_actual.profundidad >= profundidad_max:  # LÃ­mite para evitar exploraciÃ³n infinita
            continue
        
        for sucesor in reversed(estado_actual.generar_sucesores()):  # Usamos reversed para mantener el orden correcto
            if tuple(sucesor.tablero) not in visitados:
                visitados.add(tuple(sucesor.tablero))
                frontera.append(sucesor)

    return None

# reduelve por heuristica A*
def a_star(estado_inicial, estado_objetivo):
    inicial = Estado(estado_inicial, costo=distancia_manhattan(estado_inicial, estado_objetivo))
    frontera = []
    heapq.heappush(frontera, inicial)
    visitados = set()
    visitados.add(tuple(estado_inicial))

    while frontera:
        estado_actual = heapq.heappop(frontera)

        if estado_actual.tablero == estado_objetivo:
            return estado_actual

        for sucesor in estado_actual.generar_sucesores():
            if tuple(sucesor.tablero) not in visitados or sucesor.costo < estado_actual.costo + 1:
                heapq.heappush(frontera, sucesor)
                visitados.add(tuple(sucesor.tablero))

    return None


def distancia_manhattan(estado, objetivo):
    distancia = 0
    for num in range(1, 9):
        idx_actual = estado.index(num)
        idx_objetivo = objetivo.index(num)
        x1, y1 = divmod(idx_actual, 3)
        x2, y2 = divmod(idx_objetivo, 3)
        distancia += abs(x1 - x2) + abs(y1 - y2)
    return distancia

def es_solucionable(tablero):
    inversiones = 0
    tablero_lineal = [x for x in tablero if x != 0]
    for i in range(len(tablero_lineal)):
        for j in range(i + 1, len(tablero_lineal)):
            if tablero_lineal[i] > tablero_lineal[j]:
                inversiones += 1
    return inversiones % 2 == 0

def imprimir_solucion(estado_solucion):
    if estado_solucion is None:
        print("No hay soluciÃ³n para este puzzle.")
        return
    camino = []
    while estado_solucion:
        camino.append(estado_solucion)
        estado_solucion = estado_solucion.padre
    camino.reverse()
    for estado in camino:
        print(estado)
        print()

# Estado Inicial y Objetivo
estado_inicial = [1, 2, 3, 4, 6, 0, 7, 5, 8]
estado_objetivo = [1, 2, 3, 4, 5, 6, 7, 8, 0]



# Prueba BFS
print("Resolviendo con BFS:")
solucion_bfs = resolver_puzzleBFS(estado_inicial, estado_objetivo)
imprimir_solucion(solucion_bfs)

# Prueba DFS
print("Resolviendo con DFS:")
solucion_dfs = Resolver_PuzzleDFS(estado_inicial, estado_objetivo)
imprimir_solucion(solucion_dfs)

# Prueba A*
print("Resolviendo con A*:")
solucion_a_star = a_star(estado_inicial, estado_objetivo)
imprimir_solucion(solucion_a_star)


#Interfaz grÃ¡fica

"""
probando que si se suben los cambios jajaja xd lol
"""