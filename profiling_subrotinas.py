
import csv
import gc
import tracemalloc

from pathlib import Path
from statistics import median
from time import perf_counter

from src.instancia import lerInstancia
from src.distancias import construirMatrizDistancias
from src.twice_around_tree import construirAgm
from src.christofides import (
    encontrarVerticesImpares,
    calcularMatching,
    construirMultigrafo,
    construirCircuitoEuleriano,
    aplicarAtalhos,
    christofides
)
from src.branch_and_bound import calcularLimiteInferior


caminhoCatalogo = Path("data/results/catalogo_instancias.csv")

caminhoResultados = Path(
    "data/results/profiling_subrotinas.csv"
)

repeticoes = 5


def medirTempo(funcao):
    funcao()

    tempos = []

    for _ in range(repeticoes):
        gc.collect()

        inicio = perf_counter()
        resultado = funcao()
        tempo = perf_counter() - inicio

        tempos.append(tempo)

        del resultado

    return median(tempos)


def medirMemoria(funcao):
    memorias = []

    for _ in range(repeticoes):
        gc.collect()

        tracemalloc.start()

        try:
            resultado = funcao()

            _, memoriaPico = tracemalloc.get_traced_memory()

            memorias.append(
                memoriaPico / (1024 * 1024)
            )

            del resultado

        finally:
            tracemalloc.stop()

    return median(memorias)


def medirSubrotina(funcao):
    tempo = medirTempo(funcao)
    memoria = medirMemoria(funcao)

    return tempo, memoria


def registrarResultado(
    escritor,
    arquivo,
    instancia,
    subrotina,
    tempo,
    memoria
):
    escritor.writerow({
        "instancia": instancia.nome,
        "dimensao": instancia.dimensao,
        "subrotina": subrotina,
        "repeticoes": repeticoes,
        "tempoMediano": tempo,
        "memoriaMedianaMB": memoria
    })

    arquivo.flush()


def executarProfiling():
    with open(
        caminhoCatalogo,
        "r",
        newline="",
        encoding="utf-8"
    ) as arquivo:
        instancias = list(csv.DictReader(arquivo))

    campos = [
        "instancia",
        "dimensao",
        "subrotina",
        "repeticoes",
        "tempoMediano",
        "memoriaMedianaMB"
    ]

    caminhoResultados.parent.mkdir(
        parents=True,
        exist_ok=True
    )

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
            instancia = lerInstancia(registro["arquivo"])

            matriz = construirMatrizDistancias(instancia)

            print("\n" + "=" * 55)
            print("INSTÂNCIA:", instancia.nome)
            print("CIDADES:", instancia.dimensao)
            print("=" * 55)

            arvore = construirAgm(matriz)

            verticesImpares = encontrarVerticesImpares(arvore)

            matching = calcularMatching(
                verticesImpares,
                matriz
            )

            adjacencias, quantidadeArestas = construirMultigrafo(
                arvore,
                matching
            )

            circuito = construirCircuitoEuleriano(
                adjacencias,
                quantidadeArestas,
                0
            )

            funcoes = [
                (
                    "AGM",
                    lambda: construirAgm(matriz)
                ),
                (
                    "VerticesImpares",
                    lambda: encontrarVerticesImpares(arvore)
                ),
                (
                    "Matching",
                    lambda: calcularMatching(
                        verticesImpares,
                        matriz
                    )
                ),
                (
                    "Multigrafo",
                    lambda: construirMultigrafo(
                        arvore,
                        matching
                    )
                ),
                (
                    "CircuitoEuleriano",
                    lambda: construirCircuitoEuleriano(
                        adjacencias,
                        quantidadeArestas,
                        0
                    )
                ),
                (
                    "Atalhos",
                    lambda: aplicarAtalhos(
                        circuito,
                        instancia.dimensao,
                        0
                    )
                ),
                (
                    "LowerBoundRaiz",
                    lambda: calcularLimiteInferior(
                        0,
                        0,
                        list(range(1, instancia.dimensao)),
                        0,
                        matriz
                    )
                ),
                (
                    "ChristofidesCompleto",
                    lambda: christofides(matriz, 0)
                )
            ]

            for nomeSubrotina, funcao in funcoes:
                tempo, memoria = medirSubrotina(funcao)

                registrarResultado(
                    escritor,
                    arquivo,
                    instancia,
                    nomeSubrotina,
                    tempo,
                    memoria
                )

                print(
                    f"{nomeSubrotina}: "
                    f"{tempo:.6f} s | "
                    f"{memoria:.6f} MB"
                )

    print("\nProfiling concluído.")
    print("Resultados:", caminhoResultados)


if __name__ == "__main__":
    executarProfiling()
