# -*- coding: utf-8 -*-
import unittest

from ulam import sequencia


class TestSequencia(unittest.TestCase):

    def test_os_vinte_primeiros(self):
        self.assertEqual(
            sequencia.gerar(20),
            [1, 2, 3, 4, 6, 8, 11, 13, 16, 18, 26, 28, 36, 38, 47, 48, 53, 57, 62, 69])

    def test_comeca_em_um_e_dois(self):
        self.assertEqual(sequencia.gerar(1), [1])
        self.assertEqual(sequencia.gerar(2), [1, 2])

    def test_o_cinco_e_o_sete_ficam_de_fora(self):
        termos = sequencia.gerar(30)
        self.assertNotIn(5, termos, '5 = 1+4 = 2+3, duas maneiras')
        self.assertNotIn(7, termos, '7 = 1+6 = 3+4, duas maneiras')
        self.assertIn(6, termos)
        self.assertIn(8, termos)

    def test_e_estritamente_crescente(self):
        termos = sequencia.gerar(300)
        for anterior, seguinte in zip(termos, termos[1:]):
            self.assertLess(anterior, seguinte)

    def test_gerar_e_ate_concordam(self):
        por_quantidade = sequencia.gerar(200)
        por_limite = sequencia.ate(por_quantidade[-1])
        self.assertEqual(por_quantidade, por_limite)

    def test_ate_respeita_o_limite(self):
        termos = sequencia.ate(100)
        self.assertTrue(all(t <= 100 for t in termos))
        self.assertEqual(termos[-1], 99)

    def test_lacunas_sao_as_diferencas(self):
        self.assertEqual(sequencia.lacunas([1, 2, 3, 4, 6, 8]), [1, 1, 1, 2, 2])
        self.assertEqual(sequencia.lacunas([5]), [])

    def test_entrada_invalida_e_recusada(self):
        with self.assertRaises(ValueError):
            sequencia.gerar(0)
        with self.assertRaises(ValueError):
            sequencia.ate(0)


if __name__ == '__main__':
    unittest.main()
