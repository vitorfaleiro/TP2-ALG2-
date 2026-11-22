import unittest

from src.instancia import lerInstancia
from src.distancias import construirMatrizDistancias
from src.twice_around_tree import construirAgm, twiceAroundTree
from src.rotas import calcularCustoRota


class TestarTwiceAroundTree(unittest.TestCase):

    def testAgm(self):
        matriz = [
            [0, 2, 8, 10],
            [2, 0, 3, 9],
            [8, 3, 0, 4],
            [10, 9, 4, 0]
        ]

        arvore = construirAgm(matriz)

        quantidadeArestas = sum(len(vizinhos) for vizinhos in arvore) // 2

        self.assertEqual(quantidadeArestas, 3)

    def testRota(self):
        matriz = [
            [0, 2, 8, 10],
            [2, 0, 3, 9],
            [8, 3, 0, 4],
            [10, 9, 4, 0]
        ]

        rota = twiceAroundTree(matriz)

        self.assertEqual(rota, [0, 1, 2, 3, 0])
        self.assertEqual(calcularCustoRota(rota, matriz), 19)

    def testEil51(self):
        instancia = lerInstancia("data/instances/eil51.tsp")
        matriz = construirMatrizDistancias(instancia)

        rota = twiceAroundTree(matriz)

        self.assertEqual(len(rota), 52)
        self.assertEqual(rota[0], rota[-1])
        self.assertEqual(set(rota[:-1]), set(range(51)))
        self.assertEqual(len(set(rota[:-1])), 51)


if __name__ == "__main__":
    unittest.main()