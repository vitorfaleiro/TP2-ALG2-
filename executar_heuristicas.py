
import csv
from pathlib import Path
from statistics import median, mean, stdev
from time import perf_counter

from src.instancia import lerInstancia
from src.distancias import construirMatrizDistancias
from src.heuristicas import vizinhoMaisProximo
from src.twice_around_tree import twiceAroundTree
from src.christofides import christofides
from src.convex_hull import convexHullCheapestInsertion
from src.rotas import calcularCustoRota


caminhoCatalogo = Path("data/results/catalogo_instancias.csv")
caminhoResultados = Path("data/results/heuristicas.csv")

repeticoes = 5
cidadeInicial = 0


def localizarArquivo(registro):
    campos = ["arquivo", "caminho", "path", "arquivoInstancia"]

    for campo in campos:
        caminho = registro.get(campo)

        if caminho:
            caminho = Path(caminho)

            if caminho.exists():
                return caminho

    nome = registro["nome"]
    candidatos = [
        Path("data/instances/original") / f"{nome}.tsp",
        Path("data/instances/derived") / f"{nome}.tsp"
    ]

    for caminho in candidatos:
        if caminho.exists():
            return caminho

    raise FileNotFoundError(
        f"Arquivo da instância não encontrado: {nome}"
    )


def validarRota(rota, quantidadeCidades):
    return (
        len(rota) == quantidadeCidades + 1
        and rota[0] == cidadeInicial
        and rota[-1] == cidadeInicial
        and set(rota[:-1]) == set(range(quantidadeCidades))
    )


def executarAlgoritmo(funcao):
    inicio = perf_counter()
    rota = funcao()
    tempo = perf_counter() - inicio

    return rota, tempo


def medirAlgoritmo(funcao, matriz, quantidadeCidades):
    funcao()

    tempos = []
    custos = []

    for _ in range(repeticoes):
        rota, tempo = executarAlgoritmo(funcao)

        if not validarRota(rota, quantidadeCidades):
            raise ValueError("O algoritmo produziu uma rota inválida.")

        custo = calcularCustoRota(rota, matriz)

        tempos.append(tempo)
        custos.append(custo)

    if len(set(custos)) != 1:
        raise ValueError(
            "O algoritmo produziu custos diferentes entre repetições."
        )

    return {
        "custo": custos[0],
        "tempoMediano": median(tempos),
        "tempoMedio": mean(tempos),
        "desvioPadraoTempo": stdev(tempos),
        "tempoMinimo": min(tempos),
        "tempoMaximo": max(tempos)
    }


def executarExperimentos():
    with open(
        caminhoCatalogo,
        "r",
        newline="",
        encoding="utf-8"
    ) as arquivo:
        instancias = list(csv.DictReader(arquivo))

    campos = [
        "instancia",
        "tipo",
        "dimensao",
        "algoritmo",
        "cidadeInicial",
        "repeticoes",
        "custo",
        "tempoMediano",
        "tempoMedio",
        "desvioPadraoTempo",
        "tempoMinimo",
        "tempoMaximo"
    ]

    caminhoResultados.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    totalExecucoes = len(instancias) * 4

    execucaoAtual = 0

    with open(
        caminhoResultados,
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos
        )

        escritor.writeheader()
        arquivo.flush()

        for registro in instancias:
            caminhoInstancia = localizarArquivo(registro)

            instancia = lerInstancia(caminhoInstancia)

            matriz = construirMatrizDistancias(instancia)

            quantidadeCidades = instancia.dimensao

            algoritmos = [
                (
                    "Nearest Neighbor",
                    lambda: vizinhoMaisProximo(
                        matriz,
                        cidadeInicial
                    )
                ),
                (
                    "Twice-around-the-tree",
                    lambda: twiceAroundTree(
                        matriz,
                        cidadeInicial
                    )
                ),
                (
                    "Christofides",
                    lambda: christofides(
                        matriz,
                        cidadeInicial
                    ).rota
                ),
                (
                    "Convex Hull + Cheapest Insertion",
                    lambda: convexHullCheapestInsertion(
                        instancia.coordenadas,
                        matriz,
                        cidadeInicial
                    )
                )
            ]

            print("\n" + "=" * 60)
            print("INSTÂNCIA:", instancia.nome)
            print("DIMENSÃO:", quantidadeCidades)
            print("=" * 60)

            for nomeAlgoritmo, funcao in algoritmos:
                execucaoAtual += 1

                print(
                    f"\nExecução {execucaoAtual}/{totalExecucoes}"
                )

                print("Algoritmo:", nomeAlgoritmo)

                resultado = medirAlgoritmo(
                    funcao,
                    matriz,
                    quantidadeCidades
                )

                registroResultado = {
                    "instancia": instancia.nome,
                    "tipo": registro.get("tipo", ""),
                    "dimensao": quantidadeCidades,
                    "algoritmo": nomeAlgoritmo,
                    "cidadeInicial": cidadeInicial,
                    "repeticoes": repeticoes,
                    **resultado
                }

                escritor.writerow(registroResultado)
                arquivo.flush()

                print("Custo:", resultado["custo"])
                print(
                    "Tempo mediano:",
                    f'{resultado["tempoMediano"]:.6f} s'
                )

                print(
                    "Desvio padrão:",
                    f'{resultado["desvioPadraoTempo"]:.6f} s'
                )

    print("\n" + "=" * 60)
    print("EXPERIMENTOS DAS HEURÍSTICAS CONCLUÍDOS")
    print("Instâncias:", len(instancias))
    print("Algoritmos: 4")
    print("Repetições por algoritmo:", repeticoes)
    print("Total de registros:", totalExecucoes)
    print("Arquivo:", caminhoResultados)
    print("=" * 60)


if __name__ == "__main__":
    executarExperimentos()
