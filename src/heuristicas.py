def vizinhoMaisProximo(matrizDistancias, cidadeInicial=0):
    quantidadeCidades = len(matrizDistancias)

    if quantidadeCidades == 0:
        raise ValueError("A matriz de distâncias está vazia.")

    if cidadeInicial < 0 or cidadeInicial >= quantidadeCidades:
        raise ValueError("Cidade inicial inválida.")

    rota = [cidadeInicial]
    visitadas = {cidadeInicial}
    cidadeAtual = cidadeInicial

    while len(visitadas) < quantidadeCidades:
        proximaCidade = None
        menorDistancia = float("inf")

        for cidade in range(quantidadeCidades):
            if cidade not in visitadas:
                distancia = matrizDistancias[cidadeAtual][cidade]

                if distancia < menorDistancia:
                    menorDistancia = distancia
                    proximaCidade = cidade

        rota.append(proximaCidade)
        visitadas.add(proximaCidade)
        cidadeAtual = proximaCidade

    rota.append(cidadeInicial)

    return rota