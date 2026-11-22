
from time import perf_counter

from src.instancia import lerInstancia
from src.distancias import construirMatrizDistancias
from src.rotas import calcularCustoRota
from src.heuristicas import vizinhoMaisProximo
from src.twice_around_tree import twiceAroundTree
from src.christofides import christofides


instancia = lerInstancia("data/instances/eil51.tsp")
matriz = construirMatrizDistancias(instancia)

inicio = perf_counter()
rotaVizinho = vizinhoMaisProximo(matriz)
tempoVizinho = perf_counter() - inicio

inicio = perf_counter()
rotaTwice = twiceAroundTree(matriz)
tempoTwice = perf_counter() - inicio

resultadoChristofides = christofides(matriz)

print("Instância:", instancia.nome)
print("Cidades:", instancia.dimensao)
print()

print("Nearest Neighbor")
print("Custo:", calcularCustoRota(rotaVizinho, matriz))
print("Tempo:", f"{tempoVizinho:.6f} s")
print()

print("Twice-around-the-tree")
print("Custo:", calcularCustoRota(rotaTwice, matriz))
print("Tempo:", f"{tempoTwice:.6f} s")
print()

print("Christofides")
print("Custo:", resultadoChristofides.custo)
print("Tempo total:", f"{resultadoChristofides.tempoTotal:.6f} s")
print("Tempo AGM:", f"{resultadoChristofides.tempoAgm:.6f} s")
print("Tempo matching:", f"{resultadoChristofides.tempoMatching:.6f} s")
print("Tempo Euleriano:", f"{resultadoChristofides.tempoEuleriano:.6f} s")
print("Tempo atalhos:", f"{resultadoChristofides.tempoAtalhos:.6f} s")
print("Vértices ímpares:", resultadoChristofides.quantidadeImpares)
