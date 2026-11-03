# -*- coding: utf-8 -*-
"""O juiz: decide se um numero entra na sequencia contando na marra.

Nao mantem tabela, nao guarda estado, nao aproveita nada do passo anterior.
Para cada candidato, varre TODOS os pares de termos ja aceitos e conta quantos
somam o candidato. Se der exatamente um, o numero entra.

E lento de proposito. Se este caminho e o incremental concordam em todos os
termos, o incremental esta certo; se discordam em um, um dos dois esta errado,
e e ai que mora a noticia.
"""


def representacoes(numero, termos):
    """Quantos pares de termos DISTINTOS somam ``numero``, contados um a um."""
    quantos = 0
    for i in range(len(termos)):
        for j in range(i + 1, len(termos)):
            if termos[i] + termos[j] == numero:
                quantos += 1
    return quantos


def pares_que_somam(numero, termos):
    """Os pares em si, para olhar quando a conta surpreende."""
    achados = []
    for i in range(len(termos)):
        for j in range(i + 1, len(termos)):
            if termos[i] + termos[j] == numero:
                achados.append((termos[i], termos[j]))
    return achados


def gerar(quantos):
    """Os primeiros ``quantos`` termos, pelo caminho burro."""
    if quantos < 1:
        raise ValueError('quantos tem que ser positivo: %r' % (quantos,))
    termos = [1]
    if quantos == 1:
        return termos
    termos.append(2)
    candidato = 2
    while len(termos) < quantos:
        candidato += 1
        if representacoes(candidato, termos) == 1:
            termos.append(candidato)
    return termos


def eh_termo(numero, termos_anteriores):
    """True se ``numero`` entraria na sequencia depois desses termos."""
    return representacoes(numero, termos_anteriores) == 1
