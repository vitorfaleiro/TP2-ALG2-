def construirAgm(matrizDistancias):
    quantidadeCidades = len(matrizDistancias)

    if quantidadeCidades < 2:
        raise ValueError("A instância deve ter pelo menos duas cidades.")

    arvore = [[] for _ in range(quantidadeCidades)]
    visitadas = [False] * quantidadeCidades
    menoresDistancias = [float("inf")] * quantidadeCidades
    pais = [-1] * quantidadeCidades

    menoresDistancias[0] = 0

    for _ in range(quantidadeCidades):
        cidadeAtual = min(
            (i for i in range(quantidadeCidades) if not visitadas[i]),
            key=lambda i: menoresDistancias[i]
        )

        if menoresDistancias[cidadeAtual] == float("inf"):
            raise ValueError("O grafo não é conexo.")

        visitadas[cidadeAtual] = True

        if pais[cidadeAtual] != -1:
            pai = pais[cidadeAtual]
            arvore[pai].append(cidadeAtual)
            arvore[cidadeAtual].append(pai)

        for cidade in range(quantidadeCidades):
            if not visitadas[cidade]:
                distancia = matrizDistancias[cidadeAtual][cidade]

                if distancia < menoresDistancias[cidade]:
                    menoresDistancias[cidade] = distancia
                    pais[cidade] = cidadeAtual

    return arvore


def twiceAroundTree(matrizDistancias, cidadeInicial=0):
    quantidadeCidades = len(matrizDistancias)

    if not 0 <= cidadeInicial < quantidadeCidades:
        raise ValueError("Cidade inicial inválida.")

    arvore = construirAgm(matrizDistancias)

    rota = []
    visitadas = set()
    pilha = [cidadeInicial]

    while pilha:
        cidadeAtual = pilha.pop()

        if cidadeAtual in visitadas:
            continue

        visitadas.add(cidadeAtual)
        rota.append(cidadeAtual)

        for vizinho in reversed(arvore[cidadeAtual]):
            if vizinho not in visitadas:
                pilha.append(vizinho)

    rota.append(cidadeInicial)

    return rota