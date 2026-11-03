# -*- coding: utf-8 -*-
"""O padrao escondido que ninguem explica.

Em 2015, Stefan Steinerberger reparou que os numeros de Ulam, que parecem
jogados ao acaso, ficam quase todos do MESMO LADO quando multiplicados por uma
certa constante e olhados num circulo. Em numero:

    existe lambda ~ 2,5714474995 tal que cos(lambda * U_n) < 0
    para praticamente todo termo

Isso nao deveria acontecer. Uma sequencia sem estrutura teria metade dos termos
de cada lado. Nao ha prova nenhuma, nem explicacao — so a medida.

Este modulo mede isso sem supor nada: varre valores de lambda, calcula o cosseno
medio de cada um, e deixa o minimo aparecer sozinho.
"""
import math


def cosseno_medio(termos, lamb):
    """A media de cos(lambda * t) sobre os termos.

    Vale 0 para uma sequencia espalhada por igual, e -1 no extremo em que todos
    os termos caem exatamente no lado oposto.
    """
    if not termos:
        raise ValueError('a lista de termos esta vazia')
    return sum(math.cos(lamb * t) for t in termos) / len(termos)


def fracao_com_cosseno_negativo(termos, lamb):
    """Que fatia dos termos tem cos(lambda * t) < 0."""
    if not termos:
        raise ValueError('a lista de termos esta vazia')
    negativos = sum(1 for t in termos if math.cos(lamb * t) < 0)
    return negativos / len(termos)


def procurar_lambda(termos, inicio=2.0, fim=3.0, passos=2000, refinos=6):
    """Acha o lambda que deixa o cosseno medio mais negativo.

    Varredura grossa seguida de refinamentos sucessivos em volta do melhor.
    Nenhum valor de lambda e informado ao programa: ele sai da busca.

    Poucos passos com muitos refinos valem mais que muitos passos sem refino: a
    primeira versao usava 20.000 passos e 4 refinos e levava 19 segundos; 2.000
    passos e 6 refinos chegam ao mesmo lambda com mais casas, em um quinto do
    tempo. O que importa e a largura final da janela, nao a da primeira.
    """
    melhor_lamb = inicio
    melhor_valor = 1.0
    baixo, alto = inicio, fim

    for _ in range(refinos + 1):
        largura = (alto - baixo) / passos
        for i in range(passos + 1):
            lamb = baixo + i * largura
            valor = cosseno_medio(termos, lamb)
            if valor < melhor_valor:
                melhor_valor = valor
                melhor_lamb = lamb
        baixo = melhor_lamb - largura
        alto = melhor_lamb + largura

    return melhor_lamb, melhor_valor


def restos_em_fatias(termos, lamb, fatias=12):
    """Distribui os termos em fatias do circulo, por (lambda * t) modulo 2 pi.

    E o retrato de onde eles caem. Numa sequencia sem estrutura, as fatias
    ficariam todas com o mesmo tamanho.
    """
    conta = [0] * fatias
    for t in termos:
        angulo = (lamb * t) % (2 * math.pi)
        conta[int(angulo / (2 * math.pi) * fatias) % fatias] += 1
    return conta
