import unittest

from src.instancia import InstanciaTSP, lerInstancia
from src.distancias import calcularDistancia, construirMatrizDistancias


class TestarDistancias(unittest.TestCase):

    def testDistanciaConhecida(self):
        distancia = calcularDistancia((0, 0), (3, 4))
        self.assertEqual(distancia, 5)

    def testArredondamento(self):
        distancia = calcularDistancia((0, 0), (1, 1))
        self.assertEqual(distancia, 1)

    def testMatriz(self):
        instancia = InstanciaTSP(
            nome="teste",
            dimensao=3,
            tipoDistancia="EUC_2D",
            coordenadas=[(0, 0), (3, 4), (6, 8)]
        )

        matriz = construirMatrizDistancias(instancia)

        esperado = [
            [0, 5, 10],
            [5, 0, 5],
            [10, 5, 0]
        ]

        self.assertEqual(matriz, esperado)

    def testSimetriaEil51(self):
        instancia = lerInstancia("data/instances/eil51.tsp")
        matriz = construirMatrizDistancias(instancia)

        self.assertEqual(len(matriz), 51)

        for i in range(51):
            self.assertEqual(matriz[i][i], 0)

            for j in range(51):
                self.assertEqual(matriz[i][j], matriz[j][i])


if __name__ == "__main__":
    unittest.main()