
from src.heuristicas import vizinhoMaisProximo
from src.twice_around_tree import twiceAroundTree
from src.christofides import christofides
from src.convex_hull import convexHullCheapestInsertion


def gerarRotaInicial(
    matrizDistancias,
    coordenadas,
    estrategia,
    cidadeInicial=0
):
    quantidadeCidades = len(matrizDistancias)

    if estrategia == "cold":
        rota = (
            [cidadeInicial]
            + [
                cidade
                for cidade in range(quantidadeCidades)
                if cidade != cidadeInicial
            ]
            + [cidadeInicial]
        )

    elif estrategia == "nearest":
        rota = vizinhoMaisProximo(
            matrizDistancias,
            cidadeInicial
        )

    elif estrategia == "convex_hull":
        rota = convexHullCheapestInsertion(
            coordenadas,
            matrizDistancias,
            cidadeInicial
        )

    elif estrategia == "twice":
        rota = twiceAroundTree(
            matrizDistancias,
            cidadeInicial
        )

    elif estrategia == "christofides":
        resultado = christofides(
            matrizDistancias,
            cidadeInicial
        )
        rota = resultado.rota

    else:
        raise ValueError(f"Estratégia de inicialização inválida: {estrategia}")

    if (
        len(rota) != quantidadeCidades + 1
        or rota[0] != cidadeInicial
        or rota[-1] != cidadeInicial
        or set(rota[:-1]) != set(range(quantidadeCidades))
    ):
        raise ValueError("A estratégia produziu uma rota inválida.")

    return rota
