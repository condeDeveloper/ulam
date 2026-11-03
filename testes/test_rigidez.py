# -*- coding: utf-8 -*-
import math
import unittest

from ulam import rigidez, sequencia


class TestRigidez(unittest.TestCase):

    def test_cosseno_medio_de_sequencia_espalhada_fica_perto_de_zero(self):
        # os inteiros de 1 a 5000 com um lambda qualquer nao tem preferencia
        espalhada = list(range(1, 5001))
        self.assertAlmostEqual(rigidez.cosseno_medio(espalhada, 1.0), 0.0, places=2)

    def test_cosseno_medio_de_sequencia_alinhada_vale_menos_um(self):
        # multiplos de 2 pi / lambda deslocados de meia volta caem todos em -1
        lamb = 1.0
        alinhada = [math.pi + 2 * math.pi * k for k in range(50)]
        self.assertAlmostEqual(rigidez.cosseno_medio(alinhada, lamb), -1.0, places=6)

    def test_fracao_negativa_fica_entre_zero_e_um(self):
        termos = sequencia.gerar(300)
        for lamb in (1.0, 2.0, 2.5714, 3.0):
            fracao = rigidez.fracao_com_cosseno_negativo(termos, lamb)
            self.assertGreaterEqual(fracao, 0.0)
            self.assertLessEqual(fracao, 1.0)

    def test_a_busca_acha_o_lambda_sem_que_ninguem_informe(self):
        termos = sequencia.gerar(500)
        lamb, valor = rigidez.procurar_lambda(termos)
        self.assertAlmostEqual(lamb, 2.5714, places=3)
        self.assertLess(valor, -0.7)

    def test_as_fatias_somam_o_total_de_termos(self):
        termos = sequencia.gerar(400)
        fatias = rigidez.restos_em_fatias(termos, 2.5714474995, 12)
        self.assertEqual(sum(fatias), len(termos))
        self.assertEqual(len(fatias), 12)

    def test_lista_vazia_e_recusada(self):
        with self.assertRaises(ValueError):
            rigidez.cosseno_medio([], 1.0)
        with self.assertRaises(ValueError):
            rigidez.fracao_com_cosseno_negativo([], 1.0)


if __name__ == '__main__':
    unittest.main()
