
import unittest

from src.christofides import (
    encontrarVerticesImpares,
    calcularMatching,
    construirMultigrafo,
    construirCircuitoEuleriano,
    christofides
)
from src.instancia import lerInstancia
from src.distancias import construirMatrizDistancias
from src.rotas import calcularCustoRota


class TestarChristofides(unittest.TestCase):

    def testVerticesImpares(self):
        arvore = [
            [1, 2, 3],
            [0],
            [0],
            [0]
        ]

        self.assertEqual(
            encontrarVerticesImpares(arvore),
            [0, 1, 2, 3]
        )

    def testMatchingMinimo(self):
        matriz = [
            [0, 1, 10, 10],
            [1, 0, 10, 10],
            [10, 10, 0, 2],
            [10, 10, 2, 0]
        ]

        matching = calcularMatching([0, 1, 2, 3], matriz)

        pares = {frozenset(par) for par in matching}

        self.assertEqual(
            pares,
            {frozenset((0, 1)), frozenset((2, 3))}
        )

    def testCircuitoComArestasParalelas(self):
        arvore = [
            [1],
            [0]
        ]

        matching = [(0, 1)]

        adjacencias, quantidadeArestas = construirMultigrafo(
            arvore,
            matching
        )

        circuito = construirCircuitoEuleriano(
            adjacencias,
            quantidadeArestas,
            0
        )

        self.assertEqual(circuito, [0, 1, 0])

    def testRotaQuatroCidades(self):
        matriz = [
            [0, 10, 14, 10],
            [10, 0, 10, 14],
            [14, 10, 0, 10],
            [10, 14, 10, 0]
        ]

        resultado = christofides(matriz)

        self.assertEqual(resultado.custo, 40)
        self.assertEqual(len(resultado.rota), 5)
        self.assertEqual(set(resultado.rota[:-1]), set(range(4)))
        self.assertEqual(resultado.rota[0], resultado.rota[-1])

    def testEil51(self):
        instancia = lerInstancia("data/instances/eil51.tsp")
        matriz = construirMatrizDistancias(instancia)

        resultado = christofides(matriz)

        self.assertEqual(len(resultado.rota), 52)
        self.assertEqual(resultado.rota[0], resultado.rota[-1])
        self.assertEqual(set(resultado.rota[:-1]), set(range(51)))
        self.assertEqual(
            calcularCustoRota(resultado.rota, matriz),
            resultado.custo
        )

        self.assertEqual(resultado.quantidadeImpares % 2, 0)


if __name__ == "__main__":
    unittest.main()
