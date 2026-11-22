
import unittest
import random
from itertools import permutations
from math import hypot, floor

from src.branch_and_bound import branchAndBound
from src.rotas import calcularCustoRota


def gerarMatriz(quantidadeCidades, semente):
    gerador = random.Random(semente)

    coordenadas = [
        (gerador.randint(0, 100), gerador.randint(0, 100))
        for _ in range(quantidadeCidades)
    ]

    return [
        [
            floor(hypot(x1 - x2, y1 - y2) + 0.5)
            for x2, y2 in coordenadas
        ]
        for x1, y1 in coordenadas
    ]


def calcularOtimoExaustivo(matriz):
    quantidadeCidades = len(matriz)
    melhorCusto = float("inf")

    for ordem in permutations(range(1, quantidadeCidades)):
        rota = [0, *ordem, 0]
        custo = calcularCustoRota(rota, matriz)

        if custo < melhorCusto:
            melhorCusto = custo

    return melhorCusto


class TestarValidacaoExata(unittest.TestCase):

    def testCompararComForcaBruta(self):
        for quantidadeCidades in range(4, 10):
            for semente in [42, 123]:
                with self.subTest(
                    cidades=quantidadeCidades,
                    semente=semente
                ):
                    matriz = gerarMatriz(quantidadeCidades, semente)

                    otimo = calcularOtimoExaustivo(matriz)
                    resultado = branchAndBound(
                        matriz,
                        tempoLimite=10
                    )

                    self.assertEqual(resultado.status, "OTIMO")
                    self.assertEqual(resultado.custo, otimo)
                    self.assertEqual(
                        calcularCustoRota(resultado.rota, matriz),
                        resultado.custo
                    )


if __name__ == "__main__":
    unittest.main()
