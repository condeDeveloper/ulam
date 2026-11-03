# -*- coding: utf-8 -*-
"""Os numeros que estao escritos no README, presos aqui.

Se o codigo mudar e uma medida mudar junto, esta bateria quebra ANTES de o texto
virar mentira. Nenhum valor daqui foi digitado de cabeca: todos sairam do
medidor depois de a varredura terminar.
"""
import unittest

from ferramentas import medidor
from ulam import rigidez, sequencia, varredura


class TestMedidas(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.termos = sequencia.gerar(medidor.TERMOS)

    def test_o_termo_dois_mil_vale_25511(self):
        self.assertEqual(len(self.termos), 2000)
        self.assertEqual(self.termos[-1], 25511)

    def test_a_densidade_e_7_84_por_cento(self):
        d = varredura.densidade(self.termos, self.termos[-1])
        self.assertAlmostEqual(d, 0.07840, places=5)

    def test_a_densidade_cai_e_depois_se_segura(self):
        faixas = varredura.densidade_por_faixa(self.termos, 10, self.termos[-1] // 10)
        # a primeira faixa e a mais densa, e depois a coisa se acomoda
        self.assertAlmostEqual(faixas[0][3], 0.09996, places=5)
        self.assertAlmostEqual(faixas[-1][3], 0.07213, places=5)
        for _, _, _, d in faixas[1:]:
            self.assertLess(d, faixas[0][3])

    def test_pares_e_impares_quase_meio_a_meio(self):
        pares, impares = varredura.pares_e_impares(self.termos)
        self.assertEqual(pares, 994)
        self.assertEqual(impares, 1006)
        self.assertEqual(pares + impares, 2000)

    def test_so_43_diferencas_distintas_em_dois_mil_termos(self):
        conta = varredura.contagem_de_lacunas(self.termos)
        self.assertEqual(len(conta), 43)
        self.assertEqual(max(conta), 122)
        self.assertEqual(conta[2], 694)
        self.assertEqual(conta[3], 281)

    def test_a_busca_acha_a_constante_de_steinerberger(self):
        lamb, valor = rigidez.procurar_lambda(self.termos)
        self.assertAlmostEqual(lamb, 2.5714519982, places=9)
        self.assertAlmostEqual(valor, -0.792821, places=6)

    def test_99_8_por_cento_dos_termos_ficam_do_mesmo_lado(self):
        lamb, _ = rigidez.procurar_lambda(self.termos)
        fracao = rigidez.fracao_com_cosseno_negativo(self.termos, lamb)
        self.assertAlmostEqual(fracao, 0.9980, places=4)
        self.assertEqual(round(fracao * len(self.termos)), 1996)

    def test_quatro_das_doze_fatias_do_circulo_ficam_vazias(self):
        lamb, _ = rigidez.procurar_lambda(self.termos)
        fatias = rigidez.restos_em_fatias(self.termos, lamb, 12)
        self.assertEqual(fatias, [0, 0, 3, 11, 560, 605, 101, 668, 51, 1, 0, 0])
        self.assertEqual(sum(1 for f in fatias if f == 0), 4)
        # tres fatias vizinhas carregam quase tudo
        self.assertEqual(fatias[4] + fatias[5] + fatias[7], 1833)

    def test_as_tres_conferencias(self):
        self.assertEqual(varredura.conferir_contra_juiz(medidor.TERMOS_JUIZ), 120)
        pequenos = sequencia.gerar(medidor.TERMOS_JUIZ)
        self.assertEqual(varredura.conferir_representacao_unica(pequenos), 118)
        ate_600 = sequencia.ate(medidor.LIMITE_BURACOS)
        self.assertEqual(varredura.conferir_buracos(ate_600, medidor.LIMITE_BURACOS), 512)


if __name__ == '__main__':
    unittest.main()
