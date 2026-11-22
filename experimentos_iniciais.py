
import csv
from datetime import datetime
from pathlib import Path

from src.instancia import lerInstancia
from src.distancias import construirMatrizDistancias
from src.branch_and_bound import branchAndBound


instancia = lerInstancia("data/instances/eil51.tsp")
matrizCompleta = construirMatrizDistancias(instancia)

tamanhos = [22, 24, 26, 28, 30]
tempoLimite = 10

caminhoResultados = Path("data/results/experimentos_lote2.csv")
caminhoResultados.parent.mkdir(parents=True, exist_ok=True)

campos = [
    "dataExecucao",
    "instancia",
    "dimensao",
    "algoritmo",
    "warmStart",
    "tempoLimite",
    "tempoTotal",
    "tempoLimiteInferior",
    "nosExpandidos",
    "nosPodados",
    "nosCompletos",
    "melhorCusto",
    "status"
]

for tamanho in tamanhos:
    matriz = [
        linha[:tamanho]
        for linha in matrizCompleta[:tamanho]
    ]

    print(f"\nExecutando {tamanho} cidades...")

    resultado = branchAndBound(
        matriz,
        tempoLimite=tempoLimite
    )

    registro = {
        "dataExecucao": datetime.now().isoformat(timespec="seconds"),
        "instancia": f"eil51_sub{tamanho}",
        "dimensao": tamanho,
        "algoritmo": "Branch-and-Bound DFS",
        "warmStart": "Nearest Neighbor",
        "tempoLimite": tempoLimite,
        "tempoTotal": resultado.tempo,
        "tempoLimiteInferior": resultado.tempoLimiteInferior,
        "nosExpandidos": resultado.nosExpandidos,
        "nosPodados": resultado.nosPodados,
        "nosCompletos": resultado.nosCompletos,
        "melhorCusto": resultado.custo,
        "status": resultado.status
    }

    arquivoExiste = caminhoResultados.exists()

    with open(caminhoResultados, "a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)

        if not arquivoExiste or caminhoResultados.stat().st_size == 0:
            escritor.writeheader()

        escritor.writerow(registro)

    print(f"Status: {resultado.status}")
    print(f"Tempo: {resultado.tempo:.4f} s")
    print(f"Custo: {resultado.custo}")
    print(f"Nós expandidos: {resultado.nosExpandidos}")
    print(f"Nós podados: {resultado.nosPodados}")

    if resultado.status == "TIMEOUT":
        print("Limite atingido. Interrompendo os experimentos.")
        break

print("\nResultados salvos em:", caminhoResultados)
