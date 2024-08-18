import matplotlib.pyplot as plt
import numpy as np
import sys


# Escolha do arquivo a ser aberto.
try:
    caminho = sys.argv[1]
    arq = open(caminho, "r")
except:
    print(f"Erro: caminho para o arquivo nao existe ou nao foi digitado.")
    quit()

num_expansoes = {} # Guardara o numero de expansoes de cada vertice
# Guardarao os valores de F, G e H de cada vertice
f = {}
g = {}
h = {}
iteracao = [] # Lista de iteracoes. Cada iteracao eh uma tupla que contem o numero da iteracao e o no que foi expandido nela.


# Os arquivos de log mostram os dados da varredura a partir da quinta linha.
# Assim, as quatro primeiras linhas sao descartadas.

linha = arq.readline()
linha = arq.readline()
linha = arq.readline()
linha = arq.readline()
linha = arq.readline() # A quinta linha do log fica guardada

# Cada linha tem os seguintes dados, separados por tabulacoes:
#   0.  numero da thread
#   1.  numero da iteracao
#   2.  a expressao "Adding:"
#   3.  coordenada do vertice adicionado
#   4.  valor de g, h e f
linha = linha.split("\t")

# Determinacao da quantidade de dimensoes dos vertices:
dimensoes = len(linha[3].split(" "))

# Inicio da varredura dos vertices.
# A primeira linha após o relatorio com os nos comeca com "Phase 2". Assim, quando
# se detecta que o primeiro caracter da linha é "P", a varredura e encerrada.
while (linha[0][0] != "P"):
    # Pega a coordenada da linha e armazena no vetor de vertices
    no = linha[3].replace("(", "").replace(")","").split(" ")
    for i in range(len(no)):
        no[i] = int(no[i])

    no = tuple(no)

    # Registra a iteracao na lista de iteracoes e o vertice correspondente na lista de iteracoes.
    iteracao.append((int(linha[1]), no))

    # Registros de f, g e h
    proximos = linha[4].replace(")", "").split(" ")
    g[no] = int(proximos[2])
    h[no] = int(proximos[5])
    f[no] = int(proximos[8])

    # Le a proxima linha
    linha = arq.readline().split("\t")

arq.close()

# Ordenacao da lista de iteracoes
iteracao.sort()

# Geracao dos graficos

num_interacao = []
valor_f = []
valor_g = []
valor_h = []
for it in iteracao:
    num_interacao.append(it[0])
    valor_f.append(f[it[1]])
    valor_h.append(h[it[1]])
    valor_g.append(g[it[1]])


plt.plot(num_interacao, valor_f, 'y-')
plt.show()
