# -*- coding: utf-8 -*-
"""Roda as tabelas que vao para o README.

Nenhum numero daquele arquivo foi digitado a mao: todos saem daqui.

    python -m ferramentas.medidor
    python -m ferramentas.medidor --completo
"""
import sys
import time

from ulam import juiz, rigidez, sequencia, varredura

# Quantos termos as tabelas do dia a dia usam.
TERMOS = 2000

# Ate onde o juiz lento confere, termo a termo.
TERMOS_JUIZ = 120

# Ate onde conferir que nenhum numero foi pulado.
LIMITE_BURACOS = 600

# A varredura cara, que roda num job separado.
TERMOS_COMPLETO = 20000


def titulo(texto):
    print()
    print(texto)
    print('-' * len(texto))


def os_primeiros():
    titulo('Os primeiros termos, e por que os vizinhos ficaram de fora')
    termos = sequencia.gerar(20)
    print('  ' + ', '.join(str(t) for t in termos))
    print()
    print('%-8s %-14s %s' % ('numero', 'representacoes', 'pares que somam'))
    for n in range(3, 13):
        anteriores = [t for t in termos if t < n]
        pares = juiz.pares_que_somam(n, anteriores)
        marca = 'ENTRA' if len(pares) == 1 else ''
        print('%-8d %-14d %s  %s' % (
            n, len(pares),
            ' '.join('%d+%d' % p for p in pares) if pares else '(nenhum)',
            marca))


def densidade():
    titulo('Densidade, com %d termos' % TERMOS)
    termos = sequencia.gerar(TERMOS)
    maior = termos[-1]
    print('o termo %d vale %d' % (len(termos), maior))
    print('densidade ate ele: %.5f' % varredura.densidade(termos, maior))
    print()
    print('%-20s %-12s %s' % ('faixa', 'termos', 'densidade'))
    tamanho = maior // 10
    for baixo, alto, dentro, d in varredura.densidade_por_faixa(termos, 10, tamanho):
        print('%-20s %-12d %.5f' % ('%d a %d' % (baixo, alto), dentro, d))


def paridade():
    titulo('Pares e impares, com %d termos' % TERMOS)
    termos = sequencia.gerar(TERMOS)
    pares, impares = varredura.pares_e_impares(termos)
    print('pares   : %d (%.3f%%)' % (pares, 100.0 * pares / len(termos)))
    print('impares : %d (%.3f%%)' % (impares, 100.0 * impares / len(termos)))
    print()
    print('as lacunas entre vizinhos, da mais comum para a menos comum:')
    conta = varredura.contagem_de_lacunas(termos)
    for d, quantas in sorted(conta.items(), key=lambda x: -x[1])[:10]:
        print('   diferenca %-6d aparece %-8d vezes (%.2f%%)'
              % (d, quantas, 100.0 * quantas / (len(termos) - 1)))
    print()
    print('diferencas distintas no total: %d' % len(conta))
    print('a maior: %d' % max(conta))


def o_padrao():
    titulo('O padrao que ninguem explica, com %d termos' % TERMOS)
    termos = sequencia.gerar(TERMOS)
    print('procurando o lambda que deixa o cosseno medio mais negativo...')
    comeco = time.time()
    lamb, valor = rigidez.procurar_lambda(termos)
    print('lambda achado   : %.10f' % lamb)
    print('cosseno medio   : %.6f   (uma sequencia espalhada daria ~0)' % valor)
    print('termos com cos negativo: %.3f%%'
          % (100.0 * rigidez.fracao_com_cosseno_negativo(termos, lamb)))
    print('tempo da busca  : %.1f s' % (time.time() - comeco))
    print()
    print('onde os termos caem no circulo, em doze fatias:')
    fatias = rigidez.restos_em_fatias(termos, lamb, 12)
    for i, quantos in enumerate(fatias):
        barra = '#' * int(60.0 * quantos / max(fatias))
        print('   fatia %-3d %-7d %s' % (i, quantos, barra))
    vazias = sum(1 for q in fatias if q == 0)
    print()
    print('fatias vazias: %d de 12' % vazias)


def o_juiz():
    titulo('As tres conferencias')
    print('incremental x contagem na marra : %d termos iguais'
          % varredura.conferir_contra_juiz(TERMOS_JUIZ))
    termos = sequencia.gerar(TERMOS_JUIZ)
    print('todo termo com UMA representacao: %d conferidos'
          % varredura.conferir_representacao_unica(termos))
    termos_pequenos = sequencia.ate(LIMITE_BURACOS)
    print('nenhum numero pulado ate %d     : %d conferidos'
          % (LIMITE_BURACOS, varredura.conferir_buracos(termos_pequenos, LIMITE_BURACOS)))


def completo():
    titulo('Varredura com %d termos' % TERMOS_COMPLETO)
    comeco = time.time()
    termos = sequencia.gerar(TERMOS_COMPLETO)
    maior = termos[-1]
    print('o termo %d vale %d' % (len(termos), maior))
    print('densidade: %.5f' % varredura.densidade(termos, maior))
    pares, impares = varredura.pares_e_impares(termos)
    print('pares: %d   impares: %d' % (pares, impares))
    lamb, valor = rigidez.procurar_lambda(termos)
    print('lambda: %.10f   cosseno medio: %.6f' % (lamb, valor))
    print('termos com cosseno negativo: %.3f%%'
          % (100.0 * rigidez.fracao_com_cosseno_negativo(termos, lamb)))
    print()
    print('tempo: %.1f s' % (time.time() - comeco))


def main():
    if '--completo' in sys.argv:
        completo()
        return
    os_primeiros()
    densidade()
    paridade()
    o_padrao()
    o_juiz()


if __name__ == '__main__':
    main()
