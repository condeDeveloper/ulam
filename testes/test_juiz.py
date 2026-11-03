# -*- coding: utf-8 -*-
import unittest

from ulam import juiz, sequencia, varredura


class TestJuiz(unittest.TestCase):

    def test_conta_pares_distintos(self):
        termos = [1, 2, 3, 4]
        self.assertEqual(juiz.representacoes(5, termos), 2)   # 1+4 e 2+3
        self.assertEqual(juiz.representacoes(3, termos), 1)   # so 1+2
        self.assertEqual(juiz.representacoes(7, termos), 1)   # so 3+4
        self.assertEqual(juiz.representacoes(100, termos), 0)

    def test_nao_conta_o_numero_com_ele_mesmo(self):
        # 4 = 2+2 nao vale: os dois termos precisam ser distintos
        self.assertEqual(juiz.representacoes(4, [1, 2]), 0)

    def test_pares_que_somam_devolve_os_pares(self):
        self.assertEqual(juiz.pares_que_somam(5, [1, 2, 3, 4]), [(1, 4), (2, 3)])
        self.assertEqual(juiz.pares_que_somam(3, [1, 2]), [(1, 2)])

    def test_o_juiz_gera_a_mesma_sequencia(self):
        self.assertEqual(juiz.gerar(40), sequencia.gerar(40))

    def test_os_dois_caminhos_concordam_em_120_termos(self):
        self.assertEqual(varredura.conferir_contra_juiz(120), 120)

    def test_todo_termo_tem_uma_representacao(self):
        termos = sequencia.gerar(120)
        self.assertEqual(varredura.conferir_representacao_unica(termos), 118)

    def test_nenhum_numero_foi_pulado_ate_600(self):
        termos = sequencia.ate(600)
        self.assertEqual(varredura.conferir_buracos(termos, 600), 512)

    def test_entrada_invalida_e_recusada(self):
        with self.assertRaises(ValueError):
            juiz.gerar(0)


if __name__ == '__main__':
    unittest.main()
