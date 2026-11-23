
import csv
from datetime import datetime
from pathlib import Path

from src.instancia import lerInstancia
from src.distancias import construirMatrizDistancias
from src.branch_and_bound import branchAndBound


caminhoArquivo = "tests/instancias/teste_8.tsp"
tempoLimite = 30

estrategias = [
    "cold",
    "nearest",
    "convex_hull",
    "twice",
    "christofides"
]

instancia = lerInstancia(caminhoArquivo)

if instancia.tipoDistancia != "EUC_2D":
    raise ValueError("A instância deve utilizar distância EUC_2D.")

matriz = construirMatrizDistancias(instancia)

caminhoResultados = Path("data/results/experimentos_warm_start.csv")
caminhoResultados.parent.mkdir(parents=True, exist_ok=True)

campos = [
    "dataExecucao",
    "instancia",
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

arquivoExiste = caminhoResultados.exists()

with open(caminhoResultados, "a", newline="", encoding="utf-8") as arquivo:
    escritor = csv.DictWriter(arquivo, fieldnames=campos)

    if not arquivoExiste or caminhoResultados.stat().st_size == 0:
        escritor.writeheader()

    for estrategia in estrategias:
        print("\n" + "=" * 55)
        print("Estratégia:", estrategia)
        print("Instância:", instancia.nome)
        print("Dimensão:", instancia.dimensao)
        print("=" * 55)

        resultado = branchAndBound(
            matriz,
            tempoLimite=tempoLimite,
            warmStart=estrategia,
            coordenadas=instancia.coordenadas
        )

        registro = {
            "dataExecucao": datetime.now().isoformat(timespec="seconds"),
            "instancia": instancia.nome,
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

        print("Custo inicial:", resultado.custoInicial)
        print("Melhor custo:", resultado.custo)
        print("Status:", resultado.status)
        print("Tempo inicialização:", f"{resultado.tempoWarmStart:.6f} s")
        print("Tempo busca:", f"{resultado.tempoBusca:.6f} s")
        print("Tempo total:", f"{resultado.tempo:.6f} s")
        print("Memória:", f"{resultado.memoriaPicoMB:.6f} MB")
        print("Nós visitados:", resultado.nosVisitados)
        print("Nós expandidos:", resultado.nosExpandidos)
        print("Nós podados:", resultado.nosPodados)
        print("Profundidade máxima:", resultado.profundidadeMaxima)

        print("Resultado registrado no CSV.")

print("\nExperimentos concluídos.")
print("Arquivo:", caminhoResultados)
