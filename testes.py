
import random
import unittest

from ordenacao import (
    insercao,
    intercalacao,
    insercao_com_comparacoes,
    intercalacao_com_comparacoes,
)


class TestesDeOrdenacao(unittest.TestCase):

    def verificar_ordenacao(self, caso):
        """Confere o resultado dos dois algoritmos."""
        original = caso[:]
        esperado = sorted(caso)

        self.assertEqual(insercao(caso), esperado)
        self.assertEqual(intercalacao(caso), esperado)

        # Os algoritmos não devem modificar a lista original.
        self.assertEqual(caso, original)

    def test_lista_vazia(self):
        self.verificar_ordenacao([])

    def test_lista_com_um_elemento(self):
        self.verificar_ordenacao([7])

    def test_lista_com_elementos_iguais(self):
        self.verificar_ordenacao([4, 4, 4, 4, 4])

    def test_lista_ja_ordenada(self):
        self.verificar_ordenacao([1, 2, 3, 4, 5, 6])

    def test_lista_invertida(self):
        self.verificar_ordenacao([6, 5, 4, 3, 2, 1])

    def test_lista_com_valores_negativos(self):
        self.verificar_ordenacao([-10, -3, -8, 0, 5, -1])

    def test_lista_com_duplicatas(self):
        self.verificar_ordenacao([5, 2, 5, 1, 2, 1, 5, 0])

    def test_lista_com_um_valor_repetido_e_outros_diferentes(self):
        self.verificar_ordenacao([3, 3, 1, 3, 2, 3, 1])

    def test_lista_maior(self):
        caso = list(range(500, -1, -1))
        self.verificar_ordenacao(caso)

    def test_lista_aleatoria_reproduzivel(self):
        gerador = random.Random(42)

        for tamanho in [2, 5, 10, 50, 100]:
            caso = [
                gerador.randint(-1000, 1000)
                for _ in range(tamanho)
            ]

            with self.subTest(tamanho=tamanho):
                self.verificar_ordenacao(caso)

    def test_lista_com_valores_extremos(self):
        caso = [
            -10**9,
            10**9,
            0,
            -10**9,
            10**9,
        ]
        self.verificar_ordenacao(caso)

    def test_contagem_de_comparacoes_na_insercao(self):
        # Lista já ordenada: uma comparação por elemento após o primeiro.
        _, comparacoes = insercao_com_comparacoes([1, 2, 3, 4, 5])
        self.assertEqual(comparacoes, 4)

        # Lista invertida: todas as posições anteriores são comparadas.
        _, comparacoes = insercao_com_comparacoes([5, 4, 3, 2, 1])
        self.assertEqual(comparacoes, 10)

        # Lista vazia: nenhuma comparação.
        _, comparacoes = insercao_com_comparacoes([])
        self.assertEqual(comparacoes, 0)

    def test_contagem_de_comparacoes_na_intercalacao(self):
        for caso in [
            [],
            [7],
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1],
            [3, 3, 3, 3],
            [-5, 0, 8, -2, 1],
        ]:
            with self.subTest(caso=caso):
                resultado, comparacoes = (
                    intercalacao_com_comparacoes(caso)
                )

                self.assertEqual(resultado, sorted(caso))
                self.assertGreaterEqual(comparacoes, 0)

    def test_versoes_instrumentadas_produzem_resultado_correto(self):
        casos = [
            [],
            [1],
            [4, 4, 4],
            [5, 1, 3, 2, 4],
            [-10, 0, 10, -5, 5],
        ]

        for caso in casos:
            with self.subTest(caso=caso):
                original = caso[:]

                resultado_insercao, _ = (
                    insercao_com_comparacoes(caso)
                )
                resultado_intercalacao, _ = (
                    intercalacao_com_comparacoes(caso)
                )

                self.assertEqual(resultado_insercao, sorted(caso))
                self.assertEqual(resultado_intercalacao, sorted(caso))
                self.assertEqual(caso, original)


if __name__ == "__main__":
    unittest.main()
