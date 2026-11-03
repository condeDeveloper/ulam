# -*- coding: utf-8 -*-
"""Mede a sequencia: densidade, paridade, lacunas e as conferencias."""
from . import juiz, sequencia


def conferir_contra_juiz(quantos):
    """Compara o caminho incremental com a contagem na marra, termo a termo.

    Devolve quantos termos foram conferidos. Estoura se divergirem.
    """
    rapido = sequencia.gerar(quantos)
    devagar = juiz.gerar(quantos)
    if rapido != devagar:
        for i, (a, b) in enumerate(zip(rapido, devagar)):
            if a != b:
                raise AssertionError(
                    'os dois caminhos discordam no termo %d: incremental %d, juiz %d'
                    % (i + 1, a, b))
        raise AssertionError('os dois caminhos tem tamanhos diferentes')
    return len(rapido)


def conferir_representacao_unica(termos):
    """Confere que todo termo, do terceiro em diante, tem UMA representacao.

    Usa o juiz, que conta pares um a um, e nao a tabela que gerou a sequencia.
    """
    conferidos = 0
    for i in range(2, len(termos)):
        anteriores = termos[:i]
        quantas = juiz.representacoes(termos[i], anteriores)
        if quantas != 1:
            raise AssertionError(
                'o termo %d (%d) tem %d representacoes, e deveria ter uma'
                % (i + 1, termos[i], quantas))
        conferidos += 1
    return conferidos


def conferir_buracos(termos, limite):
    """Confere que todo numero FORA da sequencia tem numero de representacoes
    diferente de 1, considerando os termos menores que ele.

    E a outra metade da prova: nao basta os termos estarem certos, e preciso que
    nada tenha sido pulado.
    """
    dentro = set(termos)
    conferidos = 0
    for n in range(3, limite + 1):
        if n in dentro:
            continue
        anteriores = [t for t in termos if t < n]
        quantas = juiz.representacoes(n, anteriores)
        if quantas == 1:
            raise AssertionError(
                'o numero %d tem exatamente uma representacao e foi pulado' % n)
        conferidos += 1
    return conferidos


def densidade(termos, limite):
    """Que fatia dos inteiros ate o limite sao termos da sequencia."""
    dentro = sum(1 for t in termos if t <= limite)
    return dentro / limite


def pares_e_impares(termos):
    """Quantos termos sao pares e quantos sao impares."""
    pares = sum(1 for t in termos if t % 2 == 0)
    return pares, len(termos) - pares


def contagem_de_lacunas(termos):
    """Quantas vezes cada diferenca entre vizinhos aparece."""
    conta = {}
    for d in sequencia.lacunas(termos):
        conta[d] = conta.get(d, 0) + 1
    return conta


def densidade_por_faixa(termos, faixas, tamanho):
    """A densidade em cada bloco de ``tamanho`` inteiros, para ver se ela cai."""
    linhas = []
    for f in range(faixas):
        baixo = f * tamanho
        alto = baixo + tamanho
        dentro = sum(1 for t in termos if baixo < t <= alto)
        linhas.append((baixo + 1, alto, dentro, dentro / tamanho))
    return linhas
