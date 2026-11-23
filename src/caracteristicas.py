
from math import hypot, log, sqrt, ceil

from src.distancias import construirMatrizDistancias


def calcularAspectRatio(coordenadas):
    largura = max(x for x, _ in coordenadas) - min(
        x for x, _ in coordenadas
    )

    altura = max(y for _, y in coordenadas) - min(
        y for _, y in coordenadas
    )

    menorDimensao = min(largura, altura)

    if menorDimensao == 0:
        return None

    return max(largura, altura) / menorDimensao


def calcularFechoConvexo(coordenadas):
    pontos = sorted(set(coordenadas))

    if len(pontos) <= 1:
        return pontos

    def produtoVetorial(origem, pontoA, pontoB):
        return (
            (pontoA[0] - origem[0]) * (pontoB[1] - origem[1])
            - (pontoA[1] - origem[1]) * (pontoB[0] - origem[0])
        )

    parteInferior = []

    for ponto in pontos:
        while (
            len(parteInferior) >= 2
            and produtoVetorial(
                parteInferior[-2],
                parteInferior[-1],
                ponto
            ) <= 0
        ):
            parteInferior.pop()

        parteInferior.append(ponto)

    parteSuperior = []

    for ponto in reversed(pontos):
        while (
            len(parteSuperior) >= 2
            and produtoVetorial(
                parteSuperior[-2],
                parteSuperior[-1],
                ponto
            ) <= 0
        ):
            parteSuperior.pop()

        parteSuperior.append(ponto)

    return parteInferior[:-1] + parteSuperior[:-1]


def calcularProporcaoFechoConvexo(coordenadas):
    quantidadeCidades = len(coordenadas)

    fecho = calcularFechoConvexo(coordenadas)

    if len(fecho) == 1:
        cidadesNoFecho = sum(
            coordenada == fecho[0]
            for coordenada in coordenadas
        )

    elif len(fecho) == 2:
        pontoA, pontoB = fecho

        cidadesNoFecho = 0

        for x, y in coordenadas:
            produto = (
                (x - pontoA[0]) * (pontoB[1] - pontoA[1])
                - (y - pontoA[1]) * (pontoB[0] - pontoA[0])
            )

            dentroSegmento = (
                min(pontoA[0], pontoB[0]) <= x <= max(pontoA[0], pontoB[0])
                and min(pontoA[1], pontoB[1]) <= y <= max(pontoA[1], pontoB[1])
            )

            if produto == 0 and dentroSegmento:
                cidadesNoFecho += 1

    else:
        cidadesNoFecho = 0

        for x, y in coordenadas:
            for indice in range(len(fecho)):
                pontoA = fecho[indice]
                pontoB = fecho[(indice + 1) % len(fecho)]

                produto = (
                    (x - pontoA[0]) * (pontoB[1] - pontoA[1])
                    - (y - pontoA[1]) * (pontoB[0] - pontoA[0])
                )

                dentroSegmento = (
                    min(pontoA[0], pontoB[0]) <= x <= max(pontoA[0], pontoB[0])
                    and min(pontoA[1], pontoB[1]) <= y <= max(pontoA[1], pontoB[1])
                )

                if produto == 0 and dentroSegmento:
                    cidadesNoFecho += 1
                    break

    return cidadesNoFecho / quantidadeCidades



def calcularEntropiaEspacial(coordenadas):
    quantidadeCidades = len(coordenadas)
    quantidadeDivisoes = ceil(sqrt(quantidadeCidades))

    menorX = min(x for x, _ in coordenadas)
    maiorX = max(x for x, _ in coordenadas)

    menorY = min(y for _, y in coordenadas)
    maiorY = max(y for _, y in coordenadas)

    largura = maiorX - menorX
    altura = maiorY - menorY

    ocupacao = {}

    for x, y in coordenadas:
        if largura == 0:
            coluna = 0
        else:
            coluna = min(
                int((x - menorX) / largura * quantidadeDivisoes),
                quantidadeDivisoes - 1
            )

        if altura == 0:
            linha = 0
        else:
            linha = min(
                int((y - menorY) / altura * quantidadeDivisoes),
                quantidadeDivisoes - 1
            )

        celula = (linha, coluna)
        ocupacao[celula] = ocupacao.get(celula, 0) + 1

    entropia = 0

    for quantidade in ocupacao.values():
        probabilidade = quantidade / quantidadeCidades
        entropia -= probabilidade * log(probabilidade)

    quantidadeCelulasGrade = quantidadeDivisoes ** 2

    entropiaNormalizada = (
        entropia / log(quantidadeCelulasGrade)
    )

    return min(1.0, max(0.0, entropiaNormalizada))



def calcularGrauMaximoAgm(instancia):
    matrizDistancias = construirMatrizDistancias(instancia)

    quantidadeCidades = instancia.dimensao

    visitadas = [False] * quantidadeCidades

    menoresDistancias = [float("inf")] * quantidadeCidades

    pais = [None] * quantidadeCidades

    graus = [0] * quantidadeCidades

    menoresDistancias[0] = 0

    for _ in range(quantidadeCidades):
        cidadeAtual = min(
            (
                cidade
                for cidade in range(quantidadeCidades)
                if not visitadas[cidade]
            ),
            key=lambda cidade: menoresDistancias[cidade]
        )

        visitadas[cidadeAtual] = True

        if pais[cidadeAtual] is not None:
            graus[cidadeAtual] += 1
            graus[pais[cidadeAtual]] += 1

        for cidade in range(quantidadeCidades):
            if visitadas[cidade]:
                continue

            distancia = matrizDistancias[cidadeAtual][cidade]

            if distancia < menoresDistancias[cidade]:
                menoresDistancias[cidade] = distancia
                pais[cidade] = cidadeAtual

    return max(graus)


def calcularCvVizinhoMaisProximo(coordenadas):
    distanciasMinimas = []

    for indiceA, cidadeA in enumerate(coordenadas):
        menorDistancia = float("inf")

        for indiceB, cidadeB in enumerate(coordenadas):
            if indiceA == indiceB:
                continue

            distancia = hypot(
                cidadeA[0] - cidadeB[0],
                cidadeA[1] - cidadeB[1]
            )

            if distancia < menorDistancia:
                menorDistancia = distancia

        distanciasMinimas.append(menorDistancia)

    media = sum(distanciasMinimas) / len(distanciasMinimas)

    if media == 0:
        return None

    variancia = sum(
        (distancia - media) ** 2
        for distancia in distanciasMinimas
    ) / len(distanciasMinimas)

    desvioPadrao = sqrt(variancia)

    return desvioPadrao / media


def extrairCaracteristicas(instancia):
    coordenadas = instancia.coordenadas

    return {
        "aspectRatio": calcularAspectRatio(coordenadas),
        "proporcaoFechoConvexo": calcularProporcaoFechoConvexo(
            coordenadas
        ),
        "entropiaEspacial": calcularEntropiaEspacial(coordenadas),
        "grauMaximoAgm": calcularGrauMaximoAgm(instancia),
        "cvVizinhoMaisProximo": calcularCvVizinhoMaisProximo(
            coordenadas
        )
    }
