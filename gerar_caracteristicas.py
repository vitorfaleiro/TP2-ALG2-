
import csv
from pathlib import Path

from src.instancia import lerInstancia
from src.caracteristicas import extrairCaracteristicas


caminhoCatalogo = Path("data/results/catalogo_instancias.csv")

caminhoResultados = Path(
    "data/results/caracteristicas_instancias.csv"
)


with open(
    caminhoCatalogo,
    "r",
    newline="",
    encoding="utf-8"
) as arquivo:
    instancias = list(csv.DictReader(arquivo))


campos = [
    "nome",
    "tipo",
    "origem",
    "dimensao",
    "aspectRatio",
    "proporcaoFechoConvexo",
    "entropiaEspacial",
    "grauMaximoAgm",
    "cvVizinhoMaisProximo"
]


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

    for registro in instancias:
        instancia = lerInstancia(registro["arquivo"])

        caracteristicas = extrairCaracteristicas(instancia)

        resultado = {
            "nome": instancia.nome,
            "tipo": registro["tipo"],
            "origem": registro["origem"],
            "dimensao": instancia.dimensao,
            **caracteristicas
        }

        escritor.writerow(resultado)

        print(
            instancia.nome,
            "|",
            caracteristicas
        )


print("\nCaracterísticas calculadas para todas as instâncias.")
print("Arquivo:", caminhoResultados)
