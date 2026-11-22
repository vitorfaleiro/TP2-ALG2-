def calcularCustoRota(rota, matrizDistancias):
    custoTotal = 0

    for i in range(len(rota) - 1):
        cidadeAtual = rota[i]
        proximaCidade = rota[i + 1]

        custoTotal += matrizDistancias[cidadeAtual][proximaCidade]

    return custoTotal