import unittest

from ordenacao import insercao, intercalacao


class TestesDeOrdenacao(unittest.TestCase):
    def test_casos_dificeis(self):
        casos = [[], [7], [4, 4, 4, 4], [1, 2, 3, 4, 5], [5, 4, 3, 2, 1]]
        for caso in casos:
            with self.subTest(caso=caso):
                original = caso[:]
                esperado = sorted(caso)
                self.assertEqual(insercao(caso), esperado)
                self.assertEqual(intercalacao(caso), esperado)
                self.assertEqual(caso, original)

    def test_lista_aleatoria(self):
        caso = [8, 1, 9, 2, 7, 3, 6, 5, 4, 0]
        self.assertEqual(insercao(caso), sorted(caso))
        self.assertEqual(intercalacao(caso), sorted(caso))


if __name__ == "__main__":
    unittest.main()