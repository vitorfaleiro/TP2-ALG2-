
from dataclasses import dataclass
from time import perf_counter

import networkx as nx

from src.twice_around_tree import construirAgm
from src.rotas import calcularCustoRota


@dataclass
class ResultadoChristofides:
    rota: list[int]
    custo: int
    tempoTotal: float
    tempoAgm: float
    tempoMatching: float
    tempoEuleriano: float
    tempoAtalhos: float
    quantidadeImpares: int


def encontrarVerticesImpares(arvore):
    return [
        cidade
        for cidade, vizinhos in enumerate(arvore)
        if len(vizinhos) % 2 != 0
    ]


def calcularMatching(verticesImpares, matrizDistancias):
    grafo = nx.Graph()
    grafo.add_nodes_from(verticesImpares)

    for i in range(len(verticesImpares)):
        for j in range(i + 1, len(verticesImpares)):
            cidadeA = verticesImpares[i]
            cidadeB = verticesImpares[j]

            grafo.add_edge(
                cidadeA,
                cidadeB,
                weight=matrizDistancias[cidadeA][cidadeB]
            )

    matching = nx.algorithms.matching.min_weight_matching(
        grafo,
        weight="weight"
    )

    if len(matching) * 2 != len(verticesImpares):
        raise ValueError("Não foi encontrado matching perfeito.")

    return [tuple(par) for par in matching]


def construirMultigrafo(arvore, matching):
    quantidadeCidades = len(arvore)
    adjacencias = [[] for _ in range(quantidadeCidades)]
    identificadorAresta = 0

    def adicionarAresta(cidadeA, cidadeB):
        nonlocal identificadorAresta

        adjacencias[cidadeA].append(
            (cidadeB, identificadorAresta)
        )
        adjacencias[cidadeB].append(
            (cidadeA, identificadorAresta)
        )

        identificadorAresta += 1

    for cidade, vizinhos in enumerate(arvore):
        for vizinho in vizinhos:
            if cidade < vizinho:
                adicionarAresta(cidade, vizinho)

    for cidadeA, cidadeB in matching:
        adicionarAresta(cidadeA, cidadeB)

    return adjacencias, identificadorAresta


def construirCircuitoEuleriano(adjacencias, quantidadeArestas, cidadeInicial):
    adjacencias = [
        vizinhos.copy()
        for vizinhos in adjacencias
    ]

    arestasUtilizadas = set()
    pilha = [cidadeInicial]
    circuito = []

    while pilha:
        cidadeAtual = pilha[-1]

        while (
            adjacencias[cidadeAtual]
            and adjacencias[cidadeAtual][-1][1] in arestasUtilizadas
        ):
            adjacencias[cidadeAtual].pop()

        if adjacencias[cidadeAtual]:
            proximaCidade, identificador = adjacencias[cidadeAtual].pop()

            if identificador not in arestasUtilizadas:
                arestasUtilizadas.add(identificador)
                pilha.append(proximaCidade)
        else:
            circuito.append(pilha.pop())

    if len(arestasUtilizadas) != quantidadeArestas:
        raise ValueError("O circuito não utilizou todas as arestas.")

    circuito.reverse()

    if circuito[0] != circuito[-1]:
        raise ValueError("O circuito euleriano não foi fechado.")

    return circuito


def aplicarAtalhos(circuito, quantidadeCidades, cidadeInicial):
    visitadas = set()
    rota = []

    for cidade in circuito:
        if cidade not in visitadas:
            visitadas.add(cidade)
            rota.append(cidade)

    if len(visitadas) != quantidadeCidades:
        raise ValueError("A rota não contém todas as cidades.")

    rota.append(cidadeInicial)

    return rota


def christofides(matrizDistancias, cidadeInicial=0):
    quantidadeCidades = len(matrizDistancias)

    if quantidadeCidades < 2:
        raise ValueError("A instância deve ter pelo menos duas cidades.")

    if not 0 <= cidadeInicial < quantidadeCidades:
        raise ValueError("Cidade inicial inválida.")

    inicioTotal = perf_counter()

    inicio = perf_counter()
    arvore = construirAgm(matrizDistancias)
    tempoAgm = perf_counter() - inicio

    verticesImpares = encontrarVerticesImpares(arvore)

    inicio = perf_counter()
    matching = calcularMatching(verticesImpares, matrizDistancias)
    tempoMatching = perf_counter() - inicio

    adjacencias, quantidadeArestas = construirMultigrafo(
        arvore,
        matching
    )

    inicio = perf_counter()
    circuito = construirCircuitoEuleriano(
        adjacencias,
        quantidadeArestas,
        cidadeInicial
    )
    tempoEuleriano = perf_counter() - inicio

    inicio = perf_counter()
    rota = aplicarAtalhos(
        circuito,
        quantidadeCidades,
        cidadeInicial
    )
    tempoAtalhos = perf_counter() - inicio

    custo = calcularCustoRota(rota, matrizDistancias)
    tempoTotal = perf_counter() - inicioTotal

    return ResultadoChristofides(
        rota=rota,
        custo=custo,
        tempoTotal=tempoTotal,
        tempoAgm=tempoAgm,
        tempoMatching=tempoMatching,
        tempoEuleriano=tempoEuleriano,
        tempoAtalhos=tempoAtalhos,
        quantidadeImpares=len(verticesImpares)
    )
