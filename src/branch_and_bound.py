
from dataclasses import dataclass
from time import perf_counter
import tracemalloc

from src.rotas import calcularCustoRota
from src.inicializacao import gerarRotaInicial


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
    warmStart: str
    custoInicial: int
    tempoWarmStart: float
    tempoBusca: float
    nosVisitados: int
    nosPodadosLimiteInferior: int
    nosPodadosCustoParcial: int
    profundidadeMaxima: int
    memoriaPicoMB: float
    chamadasLimiteInferior: int


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


def branchAndBound(
    matrizDistancias,
    tempoLimite=1800,
    cidadeInicial=0,
    warmStart="nearest",
    coordenadas=None
):
    quantidadeCidades = len(matrizDistancias)

    if quantidadeCidades < 2:
        raise ValueError("A instância deve ter pelo menos duas cidades.")

    if not 0 <= cidadeInicial < quantidadeCidades:
        raise ValueError("Cidade inicial inválida.")

    if tempoLimite <= 0 or tempoLimite > 1800:
        raise ValueError("O tempo limite deve estar entre 0 e 1800 segundos.")

    if any(
        len(linha) != quantidadeCidades
        for linha in matrizDistancias
    ):
        raise ValueError("A matriz de distâncias deve ser quadrada.")

    if tracemalloc.is_tracing():
        raise RuntimeError(
            "Já existe uma medição tracemalloc ativa."
        )

    tracemalloc.start()
    tracemalloc.reset_peak()

    inicioTotal = perf_counter()

    inicioWarmStart = perf_counter()

    if warmStart == "convex_hull" and coordenadas is None:
        tracemalloc.stop()
        raise ValueError("As coordenadas são necessárias para o Convex Hull.")

    melhorRota = gerarRotaInicial(
        matrizDistancias,
        coordenadas,
        warmStart,
        cidadeInicial
    )

    tempoWarmStart = perf_counter() - inicioWarmStart

    melhorCusto = calcularCustoRota(
        melhorRota,
        matrizDistancias
    )

    custoInicial = melhorCusto

    inicioBusca = perf_counter()
    prazo = inicioTotal + tempoLimite

    nosVisitados = 0
    nosExpandidos = 0
    nosPodados = 0
    nosPodadosLimiteInferior = 0
    nosPodadosCustoParcial = 0
    nosCompletos = 0
    profundidadeMaxima = 0
    chamadasLimiteInferior = 0

    tempoLimiteInferior = 0.0
    interrompido = False

    visitadas = [False] * quantidadeCidades
    visitadas[cidadeInicial] = True

    rotaAtual = [cidadeInicial]

    def buscar(cidadeAtual, custoParcial):
        nonlocal melhorRota, melhorCusto
        nonlocal nosVisitados, nosExpandidos, nosCompletos
        nonlocal nosPodados, nosPodadosLimiteInferior
        nonlocal nosPodadosCustoParcial
        nonlocal profundidadeMaxima
        nonlocal chamadasLimiteInferior
        nonlocal tempoLimiteInferior, interrompido

        if perf_counter() >= prazo:
            interrompido = True
            return

        nosVisitados += 1

        profundidadeMaxima = max(
            profundidadeMaxima,
            len(rotaAtual) - 1
        )

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

        chamadasLimiteInferior += 1

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
            nosPodadosLimiteInferior += 1
            return

        nosExpandidos += 1

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
                nosPodadosCustoParcial += 1
                continue

            visitadas[proximaCidade] = True
            rotaAtual.append(proximaCidade)

            buscar(proximaCidade, novoCusto)

            rotaAtual.pop()
            visitadas[proximaCidade] = False

            if interrompido:
                return

    try:
        if perf_counter() >= prazo:
            interrompido = True
        else:
            buscar(cidadeInicial, 0)

        tempoBusca = perf_counter() - inicioBusca
        tempoTotal = perf_counter() - inicioTotal

        _, memoriaPico = tracemalloc.get_traced_memory()

    finally:
        tracemalloc.stop()

    memoriaPicoMB = memoriaPico / (1024 * 1024)

    return ResultadoBusca(
        rota=melhorRota,
        custo=melhorCusto,
        tempo=tempoTotal,
        tempoLimiteInferior=tempoLimiteInferior,
        nosExpandidos=nosExpandidos,
        nosPodados=nosPodados,
        nosCompletos=nosCompletos,
        status="TIMEOUT" if interrompido else "OTIMO",
        warmStart=warmStart,
        custoInicial=custoInicial,
        tempoWarmStart=tempoWarmStart,
        tempoBusca=tempoBusca,
        nosVisitados=nosVisitados,
        nosPodadosLimiteInferior=nosPodadosLimiteInferior,
        nosPodadosCustoParcial=nosPodadosCustoParcial,
        profundidadeMaxima=profundidadeMaxima,
        memoriaPicoMB=memoriaPicoMB,
        chamadasLimiteInferior=chamadasLimiteInferior
    )
