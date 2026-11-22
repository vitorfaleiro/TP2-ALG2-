
import unittest
from math import hypot, floor

from src.convex_hull import (
    construirFechoConvexo,
    convexHullCheapestInsertion
)
from src.instancia import lerInstancia
from src.distancias import construirMatrizDistancias
from src.rotas import calcularCustoRota


class TestarConvexHull(unittest.TestCase):

    def testFechoConvexo(self):
        coordenadas = [
            (0, 0),
            (2, 0),
            (2, 2),
            (0, 2),
            (1, 1)
        ]

        fecho = construirFechoConvexo(coordenadas)

        self.assertEqual(set(fecho), {0, 1, 2, 3})
        self.assertEqual(len(fecho), 4)

    def testPontosColineares(self):
        coordenadas = [
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0)
        ]

        fecho = construirFechoConvexo(coordenadas)

        self.assertEqual(set(fecho), {0, 3})

    def testRotaValida(self):
        coordenadas = [
            (0, 0),
            (2, 0),
            (2, 2),
            (0, 2),
            (1, 1)
        ]

        matriz = [
            [
                floor(hypot(x1 - x2, y1 - y2) + 0.5)
                for x2, y2 in coordenadas
            ]
            for x1, y1 in coordenadas
        ]

        rota = convexHullCheapestInsertion(
            coordenadas,
            matriz
        )

        self.assertEqual(len(rota), 6)
        self.assertEqual(set(rota[:-1]), set(range(5)))
        self.assertEqual(rota[0], rota[-1])

        custo = calcularCustoRota(rota, matriz)
        self.assertGreater(custo, 0)

    def testCidadeInicial(self):
        coordenadas = [
            (0, 0),
            (2, 0),
            (2, 2),
            (0, 2),
            (1, 1)
        ]

        matriz = [
            [
                floor(hypot(x1 - x2, y1 - y2) + 0.5)
                for x2, y2 in coordenadas
            ]
            for x1, y1 in coordenadas
        ]

        rota = convexHullCheapestInsertion(
            coordenadas,
            matriz,
            cidadeInicial=4
        )

        self.assertEqual(rota[0], 4)
        self.assertEqual(rota[-1], 4)

    def testEil51(self):
        instancia = lerInstancia("data/instances/eil51.tsp")
        matriz = construirMatrizDistancias(instancia)

        rota = convexHullCheapestInsertion(
            instancia.coordenadas,
            matriz
        )

        self.assertEqual(len(rota), 52)
        self.assertEqual(rota[0], rota[-1])
        self.assertEqual(set(rota[:-1]), set(range(51)))

    def testDimensoesIncompativeis(self):
        coordenadas = [(0, 0), (1, 1)]
        matriz = [[0, 1]]

        with self.assertRaises(ValueError):
            convexHullCheapestInsertion(coordenadas, matriz)


if __name__ == "__main__":
    unittest.main()
