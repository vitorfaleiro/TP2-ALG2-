
import unittest

from src.instancia import InstanciaTSP
from src.caracteristicas import (
    calcularAspectRatio,
    calcularProporcaoFechoConvexo,
    calcularEntropiaEspacial,
    calcularGrauMaximoAgm,
    calcularCvVizinhoMaisProximo,
    extrairCaracteristicas
)


class TestarCaracteristicas(unittest.TestCase):

    def setUp(self):
        self.coordenadas = [
            (0, 0),
            (10, 0),
            (10, 10),
            (0, 10),
            (5, 5)
        ]

        self.instancia = InstanciaTSP(
            nome="teste",
            dimensao=5,
            tipoDistancia="EUC_2D",
            coordenadas=self.coordenadas
        )

    def testAspectRatio(self):
        resultado = calcularAspectRatio(self.coordenadas)

        self.assertEqual(resultado, 1.0)

    def testProporcaoFechoConvexo(self):
        resultado = calcularProporcaoFechoConvexo(
            self.coordenadas
        )

        self.assertEqual(resultado, 0.8)


def testEntropiaEspacial(self):
    resultado = calcularEntropiaEspacial(
        self.coordenadas
    )

    self.assertGreaterEqual(resultado, 0)
    self.assertLessEqual(resultado, 1)


def testEntropiaDistribuicaoUniforme(self):
    coordenadas = [
        (0, 0),
        (10, 0),
        (0, 10),
        (10, 10)
    ]

    resultado = calcularEntropiaEspacial(coordenadas)

    self.assertAlmostEqual(resultado, 1.0)


    def testGrauMaximoAgm(self):
        resultado = calcularGrauMaximoAgm(
            self.instancia
        )

        self.assertGreaterEqual(resultado, 1)
        self.assertLessEqual(resultado, 4)

    def testCvVizinhoMaisProximo(self):
        resultado = calcularCvVizinhoMaisProximo(
            self.coordenadas
        )

        self.assertGreaterEqual(resultado, 0)

    def testExtrairCaracteristicas(self):
        resultado = extrairCaracteristicas(
            self.instancia
        )

        self.assertEqual(len(resultado), 5)

        self.assertIn("aspectRatio", resultado)
        self.assertIn("proporcaoFechoConvexo", resultado)
        self.assertIn("entropiaEspacial", resultado)
        self.assertIn("grauMaximoAgm", resultado)
        self.assertIn("cvVizinhoMaisProximo", resultado)


if __name__ == "__main__":
    unittest.main()
