
import unittest
from itertools import permutations

from src.branch_and_bound import branchAndBound
from src.rotas import calcularCustoRota


def encontrarOtimoForcaBruta(matriz):
    quantidadeCidades = len(matriz)
    melhorCusto = float("inf")

    for ordem in permutations(range(1, quantidadeCidades)):
        rota = [0] + list(ordem) + [0]
        custo = calcularCustoRota(rota, matriz)
        melhorCusto = min(melhorCusto, custo)

    return melhorCusto


class TestarBranchAndBound(unittest.TestCase):

    def testQuatroCidades(self):
        matriz = [
            [0, 10, 15, 20],
            [10, 0, 35, 25],
            [15, 35, 0, 30],
            [20, 25, 30, 0]
        ]

        resultado = branchAndBound(matriz, tempoLimite=10)

        self.assertEqual(resultado.status, "OTIMO")
        self.assertEqual(resultado.custo, 80)
        self.assertEqual(len(resultado.rota), 5)

    def testComparacaoForcaBruta(self):
        matriz = [
            [0, 4, 8, 6, 7],
            [4, 0, 5, 9, 3],
            [8, 5, 0, 2, 6],
            [6, 9, 2, 0, 4],
            [7, 3, 6, 4, 0]
        ]

        custoOtimo = encontrarOtimoForcaBruta(matriz)
        resultado = branchAndBound(matriz, tempoLimite=10)

        self.assertEqual(resultado.status, "OTIMO")
        self.assertEqual(resultado.custo, custoOtimo)
        self.assertEqual(
            calcularCustoRota(resultado.rota, matriz),
            resultado.custo
        )

    def testRotaValida(self):
        matriz = [
            [0, 3, 4, 7],
            [3, 0, 6, 2],
            [4, 6, 0, 5],
            [7, 2, 5, 0]
        ]

        resultado = branchAndBound(matriz, tempoLimite=10)

        self.assertEqual(resultado.rota[0], 0)
        self.assertEqual(resultado.rota[-1], 0)
        self.assertEqual(set(resultado.rota[:-1]), set(range(4)))
        self.assertEqual(len(resultado.rota), 5)

    def testTempoInvalido(self):
        matriz = [[0, 5], [5, 0]]

        with self.assertRaises(ValueError):
            branchAndBound(matriz, tempoLimite=0)


if __name__ == "__main__":
    unittest.main()
