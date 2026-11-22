
from time import perf_counter

from src.instancia import lerInstancia
from src.distancias import construirMatrizDistancias
from src.rotas import calcularCustoRota
from src.heuristicas import vizinhoMaisProximo
from src.twice_around_tree import twiceAroundTree
from src.christofides import christofides
from src.convex_hull import convexHullCheapestInsertion


instancia = lerInstancia("data/instances/eil51.tsp")
matriz = construirMatrizDistancias(instancia)

print("Instância:", instancia.nome)
print("Quantidade de cidades:", instancia.dimensao)
print()


inicio = perf_counter()
rotaVizinho = vizinhoMaisProximo(matriz)
tempoVizinho = perf_counter() - inicio

custoVizinho = calcularCustoRota(rotaVizinho, matriz)


inicio = perf_counter()
rotaTwice = twiceAroundTree(matriz)
tempoTwice = perf_counter() - inicio

custoTwice = calcularCustoRota(rotaTwice, matriz)


resultadoChristofides = christofides(matriz)

custoChristofides = resultadoChristofides.custo
tempoChristofides = resultadoChristofides.tempoTotal


inicio = perf_counter()
rotaConvexHull = convexHullCheapestInsertion(
    instancia.coordenadas,
    matriz
)
tempoConvexHull = perf_counter() - inicio

custoConvexHull = calcularCustoRota(rotaConvexHull, matriz)


print("Nearest Neighbor")
print("Custo:", custoVizinho)
print("Tempo:", f"{tempoVizinho:.6f} s")
print()

print("Twice-around-the-tree")
print("Custo:", custoTwice)
print("Tempo:", f"{tempoTwice:.6f} s")
print()

print("Christofides")
print("Custo:", custoChristofides)
print("Tempo total:", f"{tempoChristofides:.6f} s")
print("Tempo AGM:", f"{resultadoChristofides.tempoAgm:.6f} s")
print("Tempo matching:", f"{resultadoChristofides.tempoMatching:.6f} s")
print("Tempo Euleriano:", f"{resultadoChristofides.tempoEuleriano:.6f} s")
print("Tempo atalhos:", f"{resultadoChristofides.tempoAtalhos:.6f} s")
print("Vértices ímpares:", resultadoChristofides.quantidadeImpares)
print()

print("Convex Hull + Cheapest Insertion")
print("Custo:", custoConvexHull)
print("Tempo:", f"{tempoConvexHull:.6f} s")
print()

resultados = [
    ("Nearest Neighbor", custoVizinho, tempoVizinho),
    ("Twice-around-the-tree", custoTwice, tempoTwice),
    ("Christofides", custoChristofides, tempoChristofides),
    ("Convex Hull + Cheapest Insertion", custoConvexHull, tempoConvexHull)
]

melhorResultado = min(resultados, key=lambda resultado: resultado[1])

print("=" * 45)
print("MELHOR ROTA ENCONTRADA")
print("Algoritmo:", melhorResultado[0])
print("Custo:", melhorResultado[1])
print("Tempo:", f"{melhorResultado[2]:.6f} s")
print("=" * 45)
