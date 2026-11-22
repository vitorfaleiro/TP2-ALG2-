
from dataclasses import dataclass
from time import perf_counter

from src.heuristicas import vizinhoMaisProximo
from src.rotas import calcularCustoRota


@dataclass
class ResultadoBusca:
    rota: list[int]
    custo: int
    tempo: float
    tempoLimiteInferior: float
    nosExpandidos: int
    nosPodados: int
    nosCompletos: int
    status: str


def calcularAgmRestante(cidades, matrizDistancias):
    if len(cidades) <= 1:
        return 0

    restantes = set(cidades)
    primeiraCidade = cidades[0]
    restantes.remove(primeiraCidade)

    menoresDistancias = {
        cidade: matrizDistancias[primeiraCidade][cidade]
        for cidade in restantes
    }

    custoAgm = 0

    while restantes:
        proximaCidade = min(
            restantes,
            key=lambda cidade: menoresDistancias[cidade]
        )

        custoAgm += menoresDistancias[proximaCidade]
        restantes.remove(proximaCidade)

        for cidade in restantes:
            distancia = matrizDistancias[proximaCidade][cidade]

            if distancia < menoresDistancias[cidade]:
                menoresDistancias[cidade] = distancia

    return custoAgm


def calcularLimiteInferior(
    cidadeAtual,
    cidadeInicial,
    cidadesRestantes,
    custoParcial,
    matrizDistancias
):
    if not cidadesRestantes:
        return custoParcial + matrizDistancias[cidadeAtual][cidadeInicial]

    custoAgm = calcularAgmRestante(
        cidadesRestantes,
        matrizDistancias
    )

    conexaoAtual = min(
        matrizDistancias[cidadeAtual][cidade]
        for cidade in cidadesRestantes
    )

    conexaoInicial = min(
        matrizDistancias[cidadeInicial][cidade]
        for cidade in cidadesRestantes
    )

    return custoParcial + custoAgm + conexaoAtual + conexaoInicial


def branchAndBound(matrizDistancias, tempoLimite=1800, cidadeInicial=0):
    quantidadeCidades = len(matrizDistancias)

    if quantidadeCidades < 2:
        raise ValueError("A instância deve ter pelo menos duas cidades.")

    if not 0 <= cidadeInicial < quantidadeCidades:
        raise ValueError("Cidade inicial inválida.")

    if tempoLimite <= 0 or tempoLimite > 1800:
        raise ValueError("O tempo limite deve estar entre 0 e 1800 segundos.")

    inicio = perf_counter()
    prazo = inicio + tempoLimite

    melhorRota = vizinhoMaisProximo(matrizDistancias, cidadeInicial)
    melhorCusto = calcularCustoRota(melhorRota, matrizDistancias)

    nosExpandidos = 0
    nosPodados = 0
    nosCompletos = 0
    tempoLimiteInferior = 0.0
    interrompido = False

    visitadas = [False] * quantidadeCidades
    visitadas[cidadeInicial] = True

    rotaAtual = [cidadeInicial]

    def buscar(cidadeAtual, custoParcial):
        nonlocal melhorRota, melhorCusto
        nonlocal nosExpandidos, nosPodados, nosCompletos
        nonlocal tempoLimiteInferior, interrompido

        if perf_counter() >= prazo:
            interrompido = True
            return

        nosExpandidos += 1

        cidadesRestantes = [
            cidade
            for cidade in range(quantidadeCidades)
            if not visitadas[cidade]
        ]

        if not cidadesRestantes:
            nosCompletos += 1

            custoTotal = (
                custoParcial
                + matrizDistancias[cidadeAtual][cidadeInicial]
            )

            if custoTotal < melhorCusto:
                melhorCusto = custoTotal
                melhorRota = rotaAtual.copy() + [cidadeInicial]

            return

        inicioLimite = perf_counter()

        limiteInferior = calcularLimiteInferior(
            cidadeAtual,
            cidadeInicial,
            cidadesRestantes,
            custoParcial,
            matrizDistancias
        )

        tempoLimiteInferior += perf_counter() - inicioLimite

        if perf_counter() >= prazo:
            interrompido = True
            return

        if limiteInferior >= melhorCusto:
            nosPodados += 1
            return

        candidatos = sorted(
            cidadesRestantes,
            key=lambda cidade: (
                matrizDistancias[cidadeAtual][cidade],
                cidade
            )
        )

        for proximaCidade in candidatos:
            if perf_counter() >= prazo:
                interrompido = True
                return

            novoCusto = (
                custoParcial
                + matrizDistancias[cidadeAtual][proximaCidade]
            )

            if novoCusto >= melhorCusto:
                nosPodados += 1
                continue

            visitadas[proximaCidade] = True
            rotaAtual.append(proximaCidade)

            buscar(proximaCidade, novoCusto)

            rotaAtual.pop()
            visitadas[proximaCidade] = False

            if interrompido:
                return

    if perf_counter() >= prazo:
        interrompido = True
    else:
        buscar(cidadeInicial, 0)

    tempoTotal = perf_counter() - inicio

    return ResultadoBusca(
        rota=melhorRota,
        custo=melhorCusto,
        tempo=tempoTotal,
        tempoLimiteInferior=tempoLimiteInferior,
        nosExpandidos=nosExpandidos,
        nosPodados=nosPodados,
        nosCompletos=nosCompletos,
        status="TIMEOUT" if interrompido else "OTIMO"
    )
