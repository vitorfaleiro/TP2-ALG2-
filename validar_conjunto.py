
import csv

from src.instancia import lerInstancia
from src.distancias import construirMatrizDistancias


with open(
    "data/results/catalogo_instancias.csv",
    "r",
    encoding="utf-8"
) as arquivo:
    registros = list(csv.DictReader(arquivo))


for registro in registros:
    instancia = lerInstancia(registro["arquivo"])
    matriz = construirMatrizDistancias(instancia)

    assert instancia.tipoDistancia == "EUC_2D"
    assert len(matriz) == instancia.dimensao
    assert all(len(linha) == instancia.dimensao for linha in matriz)

    print(
        instancia.nome,
        "| Cidades:", instancia.dimensao,
        "| Matriz:", len(matriz), "x", len(matriz),
        "| OK"
    )

print("\nTodas as instâncias foram validadas.")
