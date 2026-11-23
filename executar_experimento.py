
import csv
import os
from datetime import datetime
from pathlib import Path

from src.instancia import lerInstancia
from src.distancias import construirMatrizDistancias
from src.branch_and_bound import branchAndBound


caminhoCatalogo = Path("data/results/catalogo_instancias.csv")
caminhoResultados = Path("data/results/experimentos_oficiais.csv")

tempoLimite = 1800

estrategias = [
    "cold",
    "nearest",
    "convex_hull",
    "twice",
    "christofides"
]

campos = [
    "dataExecucao",
    "instancia",
    "tipoInstancia",
    "origem",
    "dimensao",
    "algoritmo",
    "warmStart",
    "tempoLimite",
    "tempoInicializacao",
    "tempoBusca",
    "tempoTotal",
    "tempoLowerBound",
    "memoriaPicoMB",
    "nosVisitados",
    "nosExpandidos",
    "nosCompletos",
    "nosPodados",
    "nosPodadosLimiteInferior",
    "nosPodadosCustoParcial",
    "profundidadeMaxima",
    "custoInicial",
    "melhorCusto",
    "status"
]


def localizarArquivo(registro):
    if registro.get("arquivo"):
        caminho = Path(registro["arquivo"])

        if caminho.exists():
            return caminho

    nome = registro["nome"]

    pastas = [
        Path("data/instances/original"),
        Path("data/instances/derived")
    ]

    for pasta in pastas:
        caminho = pasta / f"{nome}.tsp"

        if caminho.exists():
            return caminho

    raise FileNotFoundError(
        f"Arquivo da instância {nome} não encontrado."
    )


def carregarExecucoesConcluidas():
    concluidas = set()

    if not caminhoResultados.exists():
        return concluidas

    with open(
        caminhoResultados,
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as arquivo:
        leitor = csv.DictReader(arquivo)

        if leitor.fieldnames != campos:
            raise ValueError(
                "O cabeçalho do CSV existente não corresponde "
                "ao formato esperado. Nenhum resultado foi alterado."
            )

        for registro in leitor:
            if registro["status"] in ("OTIMO", "TIMEOUT"):
                identificador = (
                    registro["instancia"],
                    registro["warmStart"]
                )

                concluidas.add(identificador)

    return concluidas


def registrarResultado(
    escritor,
    arquivo,
    instancia,
    tipo,
    origem,
    estrategia,
    resultado
):
    registro = {
        "dataExecucao": datetime.now().isoformat(timespec="seconds"),
        "instancia": instancia.nome,
        "tipoInstancia": tipo,
        "origem": origem,
        "dimensao": instancia.dimensao,
        "algoritmo": "Branch-and-Bound DFS",
        "warmStart": estrategia,
        "tempoLimite": tempoLimite,
        "tempoInicializacao": resultado.tempoWarmStart,
        "tempoBusca": resultado.tempoBusca,
        "tempoTotal": resultado.tempo,
        "tempoLowerBound": resultado.tempoLimiteInferior,
        "memoriaPicoMB": resultado.memoriaPicoMB,
        "nosVisitados": resultado.nosVisitados,
        "nosExpandidos": resultado.nosExpandidos,
        "nosCompletos": resultado.nosCompletos,
        "nosPodados": resultado.nosPodados,
        "nosPodadosLimiteInferior": resultado.nosPodadosLimiteInferior,
        "nosPodadosCustoParcial": resultado.nosPodadosCustoParcial,
        "profundidadeMaxima": resultado.profundidadeMaxima,
        "custoInicial": resultado.custoInicial,
        "melhorCusto": resultado.custo,
        "status": resultado.status
    }

    escritor.writerow(registro)

    arquivo.flush()
    os.fsync(arquivo.fileno())


def executar():
    if not caminhoCatalogo.exists():
        raise FileNotFoundError(
            "Catálogo de instâncias não encontrado."
        )

    with open(
        caminhoCatalogo,
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as arquivo:
        instancias = list(csv.DictReader(arquivo))

    concluidas = carregarExecucoesConcluidas()

    totalExecucoes = len(instancias) * len(estrategias)

    execucoesRestantes = sum(
        (registro["nome"], estrategia) not in concluidas
        for registro in instancias
        for estrategia in estrategias
    )

    caminhoResultados.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    arquivoExiste = (
        caminhoResultados.exists()
        and caminhoResultados.stat().st_size > 0
    )

    print("=" * 60)
    print("EXPERIMENTOS OFICIAIS - BRANCH AND BOUND")
    print("=" * 60)
    print("Instâncias:", len(instancias))
    print("Estratégias:", len(estrategias))
    print("Total de execuções:", totalExecucoes)
    print("Execuções já concluídas:", len(concluidas))
    print("Execuções restantes:", execucoesRestantes)
    print("Limite por execução:", tempoLimite, "segundos")
    print("=" * 60, flush=True)

    with open(
        caminhoResultados,
        "a",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos
        )

        if not arquivoExiste:
            escritor.writeheader()
            arquivo.flush()
            os.fsync(arquivo.fileno())

        numeroExecucao = 0

        for registro in instancias:
            caminhoInstancia = localizarArquivo(registro)

            instancia = lerInstancia(caminhoInstancia)

            matriz = construirMatrizDistancias(instancia)

            tipo = (
                registro.get("tipo")
                or registro.get("tipoInstancia")
                or "original"
            )

            origem = (
                registro.get("origem")
                or ("TSPLIB" if tipo == "original" else "TSPLIB derivada")
            )

            for estrategia in estrategias:
                numeroExecucao += 1

                identificador = (
                    instancia.nome,
                    estrategia
                )

                if identificador in concluidas:
                    print(
                        f"[PULADA] {instancia.nome} - {estrategia}",
                        flush=True
                    )
                    continue

                print("\n" + "=" * 60)
                print(
                    f"EXECUÇÃO {numeroExecucao}/{totalExecucoes}"
                )
                print("Instância:", instancia.nome)
                print("Dimensão:", instancia.dimensao)
                print("Origem:", tipo, origem)
                print("Estratégia:", estrategia)
                print("=" * 60, flush=True)

                resultado = branchAndBound(
                    matriz,
                    tempoLimite=tempoLimite,
                    warmStart=estrategia,
                    coordenadas=instancia.coordenadas
                )

                registrarResultado(
                    escritor,
                    arquivo,
                    instancia,
                    tipo,
                    origem,
                    estrategia,
                    resultado
                )

                concluidas.add(identificador)

                print("\nRESULTADO")
                print("Status:", resultado.status)
                print("Custo inicial:", resultado.custoInicial)
                print("Melhor custo:", resultado.custo)
                print(
                    "Tempo total:",
                    f"{resultado.tempo:.4f} segundos"
                )
                print(
                    "Memória:",
                    f"{resultado.memoriaPicoMB:.4f} MB"
                )
                print("Nós visitados:", resultado.nosVisitados)
                print("Nós expandidos:", resultado.nosExpandidos)
                print("Nós podados:", resultado.nosPodados)
                print("Profundidade:", resultado.profundidadeMaxima)
                print("Resultado salvo no CSV.", flush=True)

    print("\n" + "=" * 60)
    print("EXECUÇÕES FINALIZADAS")
    print("Arquivo:", caminhoResultados)
    print("=" * 60)


if __name__ == "__main__":
    executar()
