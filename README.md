# ulam

Comece com **1** e **2**. Daí em diante, o próximo termo é o menor inteiro maior que o
último que pode ser escrito como soma de dois termos anteriores **de exatamente uma
maneira**.

```
1, 2, 3, 4, 6, 8, 11, 13, 16, 18, 26, 28, 36, 38, 47, 48, 53, 57, 62, 69, ...
```

O `5` fica de fora porque `5 = 1+4 = 2+3`. O `7` fica de fora porque `7 = 1+6 = 3+4`. O
`3` entra porque só existe `1+2`.

A regra cabe numa linha e a sequência é um caos: ninguém sabe provar nem que ela tem
densidade positiva. Mas ela esconde um padrão que, até hoje, ninguém explicou — e este
repositório o encontra **sem que ele seja informado ao programa**.

```bash
python -m unittest discover -s testes -t . -v   # 31 testes
python -m ferramentas.medidor                   # todas as tabelas
python -m ferramentas.medidor --completo        # 20.000 termos (job próprio)
```

Python 3.11+, sem dependência nenhuma fora da biblioteca padrão.

## Os primeiros, e por que os vizinhos ficaram de fora

```
número   representações   pares que somam
3        1                1+2            ENTRA
4        1                1+3            ENTRA
5        2                1+4  2+3
6        1                2+4            ENTRA
7        2                1+6  3+4
8        1                2+6            ENTRA
9        2                1+8  3+6
10       2                2+8  4+6
11       1                3+8            ENTRA
12       2                1+11 4+8
```

## Três conferências

A sequência é gerada por um caminho **incremental**, que mantém uma tabela de quantas
representações cada inteiro já tem e a atualiza quando um termo novo entra. O juiz não
mantém nada: para cada candidato, varre **todos os pares** de termos aceitos e conta.

```
incremental x contagem na marra  : 120 termos iguais
todo termo com UMA representação : 118 conferidos
nenhum número pulado até 600     : 512 conferidos
```

A terceira linha é a metade que se esquece. Não basta que os termos aceitos estejam
certos — é preciso que **nada tenha sido deixado para trás**. Para cada um dos 512
números que ficaram de fora até 600, o juiz confirma que o número de representações é
diferente de 1.

## O padrão que ninguém explica

Em 2015, Stefan Steinerberger reparou que os números de Ulam, aparentemente jogados ao
acaso, ficam quase todos do **mesmo lado** quando multiplicados por uma certa constante e
olhados num círculo.

Este repositório não recebe essa constante. Ele varre valores de λ entre 2 e 3, calcula o
cosseno médio de cada um, e deixa o mínimo aparecer:

```
λ encontrado  : 2,5714519982
cosseno médio : -0,792821     (uma sequência espalhada daria ~0)
termos com cos(λ·t) < 0 : 99,800%   —  1996 de 2000
```

E o retrato de onde eles caem, em doze fatias do círculo:

```
fatia  0      0
fatia  1      0
fatia  2      3
fatia  3     11
fatia  4    560   ##################################################
fatia  5    605   ######################################################
fatia  6    101   #########
fatia  7    668   ############################################################
fatia  8     51   ####
fatia  9      1
fatia 10      0
fatia 11      0
```

**Quatro das doze fatias ficam completamente vazias**, e três fatias vizinhas carregam
1.833 dos 2.000 termos. Uma sequência sem estrutura teria 167 em cada fatia.

Não há prova disso. Não há explicação. Há a medida.

## Densidade e lacunas

```
faixa              termos   densidade
1 a 2551           255      0,09996
2552 a 5102        208      0,08154
5103 a 7653        187      0,07330
...
22960 a 25510      184      0,07213
```

A densidade cai da primeira faixa e depois **se segura** em torno de 7,5% em vez de
continuar caindo. Com 2.000 termos, o último vale 25.511 e a densidade geral é **7,84%**.

As diferenças entre termos vizinhos são o detalhe mais estranho:

```
diferença 2    aparece 694 vezes   (34,72%)
diferença 3    aparece 281 vezes   (14,06%)
diferença 17   aparece 162 vezes   ( 8,10%)
diferença 20   aparece 129 vezes   ( 6,45%)
diferença 25   aparece 109 vezes   ( 5,45%)
```

Em 2.000 termos espalhados por 25 mil inteiros, existem apenas **43 diferenças
distintas**, e a maior delas é **122**. Mais de um terço dos saltos é de exatamente 2.

## O que as medidas me corrigiram

**Chutei o último termo de uma faixa e errei.** Escrevi num teste que o maior termo até
100 seria `97`. É **99** — os dois estão na sequência, e eu parei de contar no penúltimo.
O teste pegou na primeira execução, que é exatamente para isso que ele existe.

**Esperei a paridade desequilibrada.** Olhando os primeiros termos (`2, 4, 6, 8, 18, 26,
28, 36, 38, 48`) a impressão é de que os pares dominam. Com 2.000 termos são **994 pares
contra 1.006 ímpares** — meio a meio, com meio por cento de diferença.

**Gastei 19 segundos procurando λ do jeito errado.** A primeira busca usava 20.000 passos
numa varredura grossa e 4 refinamentos. Trocando para **2.000 passos e 6 refinamentos**, o
λ sai idêntico até a décima casa em **2,9 segundos**. O que determina a precisão é a
largura da **última** janela, não a da primeira — gastar passos na varredura inicial é
pagar caro por algo que o refino entrega de graça.

**Quase chutei a densidade.** A primeira faixa dá 9,996% e a impressão é de uma queda
contínua. As nove faixas seguintes ficam entre 7,1% e 8,4%, subindo e descendo. Escrever
"a densidade cai" seria verdade só no primeiro passo.

## Quatro achados

1. **A busca encontra a constante sozinha.** Sem receber nenhum valor, a varredura chega a
   **λ = 2,5714519982**, e com ele **99,800% dos termos** — 1.996 de 2.000 — caem do mesmo
   lado do círculo.
2. **Quatro das doze fatias do círculo ficam vazias**, e três fatias vizinhas concentram
   **1.833 dos 2.000** termos. O esperado para uma sequência sem estrutura seria 167 por
   fatia.
3. Em 2.000 termos espalhados por 25.511 inteiros existem apenas **43 diferenças
   distintas** entre vizinhos, a maior é **122**, e a diferença **2 sozinha responde por
   34,72%** dos saltos.
4. A paridade é quase exata — **994 pares contra 1.006 ímpares** — e a densidade, depois
   de cair de 9,996% na primeira faixa, **se segura** em torno de 7,5% em vez de continuar
   caindo.
