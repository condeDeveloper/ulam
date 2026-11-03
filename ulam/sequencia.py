# -*- coding: utf-8 -*-
"""A sequencia de Ulam.

Comece com 1 e 2. Daí em diante, o proximo termo e o MENOR inteiro maior que o
ultimo que pode ser escrito como soma de dois termos anteriores DISTINTOS de
exatamente UMA maneira.

    1, 2, 3, 4, 6, 8, 11, 13, 16, 18, 26, 28, 36, 38, 47, ...

O 5 fica de fora porque 5 = 1+4 = 2+3, duas maneiras. O 7 fica de fora porque
7 = 1+6 = 3+4. O 3 entra porque so ha 3 = 1+2.

A regra e simples e a sequencia e caotica: ninguem sabe provar nem que ela tem
densidade positiva, nem explicar o padrao que ela esconde modulo uma constante
estranha (veja o modulo `rigidez`).
"""


def gerar(quantos):
    """Os primeiros ``quantos`` termos, pelo caminho incremental.

    Mantem uma tabela de quantas representacoes cada inteiro tem como soma de
    dois termos distintos ja aceitos. Quando um termo novo entra, ele soma com
    todos os anteriores e incrementa a tabela — nada e recalculado do zero.
    """
    if quantos < 1:
        raise ValueError('quantos tem que ser positivo: %r' % (quantos,))
    termos = [1]
    if quantos == 1:
        return termos
    termos.append(2)

    # representacoes[n] = de quantas maneiras n e soma de dois termos distintos
    representacoes = {3: 1}
    candidato = 2

    while len(termos) < quantos:
        candidato += 1
        while representacoes.get(candidato, 0) != 1:
            candidato += 1
            if candidato > 10 ** 9:
                raise RuntimeError('a busca passou de um bilhao sem achar termo')
        termos.append(candidato)
        for anterior in termos[:-1]:
            soma = anterior + candidato
            representacoes[soma] = representacoes.get(soma, 0) + 1

    return termos


def ate(limite):
    """Todos os termos menores ou iguais a ``limite``."""
    if limite < 1:
        raise ValueError('limite tem que ser positivo: %r' % (limite,))
    termos = [1]
    if limite < 2:
        return termos
    termos.append(2)
    representacoes = {3: 1}
    candidato = 2

    while True:
        candidato += 1
        if candidato > limite:
            return termos
        if representacoes.get(candidato, 0) != 1:
            continue
        termos.append(candidato)
        for anterior in termos[:-1]:
            soma = anterior + candidato
            if soma <= limite:
                representacoes[soma] = representacoes.get(soma, 0) + 1


def lacunas(termos):
    """As diferencas entre termos vizinhos."""
    return [b - a for a, b in zip(termos, termos[1:])]
