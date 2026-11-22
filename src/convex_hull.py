
def calcularProdutoVetorial(pontoA, pontoB, pontoC):
    return (
        (pontoB[0] - pontoA[0]) * (pontoC[1] - pontoA[1])
        - (pontoB[1] - pontoA[1]) * (pontoC[0] - pontoA[0])
    )


def construirFechoConvexo(coordenadas):
    pontos = sorted(
        (x, y, indice)
        for indice, (x, y) in enumerate(coordenadas)
    )

    if len(pontos) <= 2:
        return [ponto[2] for ponto in pontos]

    inferior = []

    for ponto in pontos:
        while (
            len(inferior) >= 2
            and calcularProdutoVetorial(
                inferior[-2],
                inferior[-1],
                ponto
            ) <= 0
        ):
            inferior.pop()

        inferior.append(ponto)

    superior = []

    for ponto in reversed(pontos):
        while (
            len(superior) >= 2
            and calcularProdutoVetorial(
                superior[-2],
                superior[-1],
                ponto
            ) <= 0
        ):
            superior.pop()

        superior.append(ponto)

    fecho = inferior[:-1] + superior[:-1]

    return [ponto[2] for ponto in fecho]



def convexHullCheapestInsertion(
    coordenadas,
    matrizDistancias,
    cidadeInicial=0
):
    quantidadeCidades = len(coordenadas)

    if quantidadeCidades < 2:
        raise ValueError("A instância deve ter pelo menos duas cidades.")

    if (
        len(matrizDistancias) != quantidadeCidades
        or any(len(linha) != quantidadeCidades for linha in matrizDistancias)
    ):
        raise ValueError("Dimensões incompatíveis entre coordenadas e matriz.")

    if not 0 <= cidadeInicial < quantidadeCidades:
        raise ValueError("Cidade inicial inválida.")

    rota = construirFechoConvexo(coordenadas)
    visitadas = set(rota)

    while len(visitadas) < quantidadeCidades:
        melhorInsercao = None

        for cidade in range(quantidadeCidades):
            if cidade in visitadas:
                continue

            for i in range(len(rota)):
                cidadeA = rota[i]
                cidadeB = rota[(i + 1) % len(rota)]

                aumento = (
                    matrizDistancias[cidadeA][cidade]
                    + matrizDistancias[cidade][cidadeB]
                    - matrizDistancias[cidadeA][cidadeB]
                )

                candidata = (aumento, cidade, i)

                if (
                    melhorInsercao is None
                    or candidata < melhorInsercao
                ):
                    melhorInsercao = candidata

        _, cidadeEscolhida, posicao = melhorInsercao

        rota.insert(posicao + 1, cidadeEscolhida)
        visitadas.add(cidadeEscolhida)

    indiceInicial = rota.index(cidadeInicial)
    rota = rota[indiceInicial:] + rota[:indiceInicial]

    rota.append(cidadeInicial)

    return rota
