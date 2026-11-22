
import csv
from datetime import datetime
from pathlib import Path

from src.instancia import lerInstancia
from src.distancias import construirMatrizDistancias
from src.branch_and_bound import branchAndBound


caminhoArquivo = "tests/instancias/teste_8.tsp"

instancia = lerInstancia(caminhoArquivo)
matriz = construirMatrizDistancias(instancia)

resultado = branchAndBound(matriz, tempoLimite=30)

print("Instância:", instancia.nome)
print("Custo:", resultado.custo)
print("Status:", resultado.status)
print("Tempo:", round(resultado.tempo, 6), "s")
print("Tempo lower bound:", round(resultado.tempoLimiteInferior, 6), "s")
print("Nós expandidos:", resultado.nosExpandidos)
print("Nós podados:", resultado.nosPodados)
print("Nós completos:", resultado.nosCompletos)
print("Rota:", [cidade + 1 for cidade in resultado.rota])

caminhoResultados = Path("data/results/branch_and_bound.csv")
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

registro = {
    "dataExecucao": datetime.now().isoformat(timespec="seconds"),
    "instancia": instancia.nome,
    "dimensao": instancia.dimensao,
    "algoritmo": "Branch-and-Bound DFS",
    "warmStart": "Nearest Neighbor",
    "tempoLimite": 30,
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

print("Resultado registrado em:", caminhoResultados)
