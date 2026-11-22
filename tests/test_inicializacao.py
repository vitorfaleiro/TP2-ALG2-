
import unittest
from math import hypot, floor

from src.inicializacao import gerarRotaInicial
from src.branch_and_bound import branchAndBound


class TestarInicializacao(unittest.TestCase):

    def setUp(self):
        self.coordenadas = [
            (0, 0),
            (10, 0),
            (10, 10),
            (0, 10),
            (5, 5)
        ]

        self.matriz = [
            [
                floor(hypot(x1 - x2, y1 - y2) + 0.5)
                for x2, y2 in self.coordenadas
            ]
            for x1, y1 in self.coordenadas
        ]

        self.estrategias = [
            "cold",
            "nearest",
            "convex_hull",
            "twice",
            "christofides"
        ]

    def testTodasEstrategiasGeramRotaValida(self):
        for estrategia in self.estrategias:
            with self.subTest(estrategia=estrategia):
                rota = gerarRotaInicial(
                    self.matriz,
                    self.coordenadas,
                    estrategia
                )

                self.assertEqual(len(rota), 6)
                self.assertEqual(rota[0], 0)
                self.assertEqual(rota[-1], 0)
                self.assertEqual(set(rota[:-1]), set(range(5)))

    def testTodasEstrategiasNoBranchAndBound(self):
        for estrategia in self.estrategias:
            with self.subTest(estrategia=estrategia):
                resultado = branchAndBound(
                    self.matriz,
                    tempoLimite=10,
                    warmStart=estrategia,
                    coordenadas=self.coordenadas
                )

                self.assertEqual(resultado.status, "OTIMO")
                self.assertEqual(resultado.custo, 44)
                self.assertGreaterEqual(
                    resultado.custoInicial,
                    resultado.custo
                )

    def testEstrategiaInvalida(self):
        with self.assertRaises(ValueError):
            gerarRotaInicial(
                self.matriz,
                self.coordenadas,
                "inexistente"
            )

    def testConvexHullSemCoordenadas(self):
        with self.assertRaises(ValueError):
            branchAndBound(
                self.matriz,
                tempoLimite=10,
                warmStart="convex_hull"
            )


if __name__ == "__main__":
    unittest.main()
