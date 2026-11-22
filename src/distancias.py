from math import hypot, floor


def calcularDistancia(cidadeA, cidadeB):
    x1, y1 = cidadeA
    x2, y2 = cidadeB

    distancia = hypot(x2 - x1, y2 - y1)

    return floor(distancia + 0.5)


def construirMatrizDistancias(instancia):
    dimensao = instancia.dimensao
    matriz = [[0] * dimensao for _ in range(dimensao)]

    for i in range(dimensao):
        for j in range(i + 1, dimensao):
            distancia = calcularDistancia(
                instancia.coordenadas[i],
                instancia.coordenadas[j]
            )

            matriz[i][j] = distancia
            matriz[j][i] = distancia

    return matriz