
import csv
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
    "chamadasLimiteInferior",
    "status"
]


def carregarExecucoesConcluidas():
    concluidas = set()

    if not caminhoResultados.exists():
        return concluidas

    with open(
        caminhoResultados,
        "r",
        newline="",
        encoding="utf-8"
    ) as arquivo:
        leitor = csv.DictReader(arquivo)

        for registro in leitor:
            if registro["status"] in ("OTIMO", "TIMEOUT"):
                concluidas.add((
                    registro["instancia"],
                    registro["warmStart"]
                ))

    return concluidas


def registrarResultado(escritor, arquivo, instancia, tipo, origem, estrategia, resultado):
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
        "chamadasLimiteInferior": resultado.chamadasLimiteInferior,
        "status": resultado.status
    }

    escritor.writerow(registro)
    arquivo.flush()


def executar():
    if not caminhoCatalogo.exists():
        raise FileNotFoundError("Catálogo de instâncias não encontrado.")

    with open(
        caminhoCatalogo,
        "r",
        newline="",
        encoding="utf-8"
    ) as arquivo:
        instancias = list(csv.DictReader(arquivo))

    concluidas = carregarExecucoesConcluidas()

    caminhoResultados.parent.mkdir(parents=True, exist_ok=True)

    arquivoExiste = (
        caminhoResultados.exists()
        and caminhoResultados.stat().st_size > 0
    )

    totalExecucoes = len(instancias) * len(estrategias)
    execucoesRestantes = sum(
        (registro["nome"], estrategia) not in concluidas
        for registro in instancias
        for estrategia in estrategias
    )

    print("=" * 60)
    print("EXPERIMENTOS OFICIAIS - BRANCH AND BOUND")
    print("=" * 60)
    print("Instâncias:", len(instancias))
    print("Estratégias:", len(estrategias))
    print("Total de execuções:", totalExecucoes)
    print("Execuções restantes:", execucoesRestantes)
    print("Limite por execução:", tempoLimite, "segundos")
    print("=" * 60)

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

        numeroExecucao = 0

        for registro in instancias:
            nomeArquivo = registro["arquivo"]
            tipo = registro["tipo"]
            origem = registro["origem"]

            instancia = lerInstancia(nomeArquivo)

            if instancia.tipoDistancia != "EUC_2D":
                raise ValueError(
                    f"Tipo de distância incompatível: {instancia.nome}"
                )

            matriz = construirMatrizDistancias(instancia)

            for estrategia in estrategias:
                numeroExecucao += 1

                identificador = (
                    instancia.nome,
                    estrategia
                )

                if identificador in concluidas:
                    print(
                        f"\n[PULADA] {instancia.nome} - {estrategia}"
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
                print("=" * 60)

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
                    f"{resultado.tempo:.4f} s"
                )
                print(
                    "Memória:",
                    f"{resultado.memoriaPicoMB:.4f} MB"
                )
                print("Nós visitados:", resultado.nosVisitados)
                print("Nós expandidos:", resultado.nosExpandidos)
                print("Nós podados:", resultado.nosPodados)
                print("Profundidade:", resultado.profundidadeMaxima)
                print("Resultado salvo no CSV.")

    print("\n" + "=" * 60)
    print("EXECUÇÕES FINALIZADAS")
    print("Arquivo:", caminhoResultados)
    print("=" * 60)


if __name__ == "__main__":
    executar()
