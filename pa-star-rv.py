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
saltos = [] # Lista de saltos
num_saltos = 0 # Quantidade de saltos
iteracao = [] # Lista de iteracoes. Cada iteracao eh uma tupla que contem o numero da iteracao e o no que foi expandido nela.
med_h_vizinhos = {} # Guardara a media dos valores de H dos vizinhos de cada no

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

# Define a funcao recursiva que retorna os vizinhos de um vertice
def get_vizinhos(vertice, lista_viz, indice):
    if indice <= 0:
        lista_viz.append(vertice)
        novo_vertice = list(vertice)
        novo_vertice[indice] += 1
        lista_viz.append(tuple(novo_vertice))
        if novo_vertice[indice] > 1:
            novo_vertice[indice] -= 2
            lista_viz.append(tuple(novo_vertice))
        return lista_viz

    lista_viz.append(vertice)
    lista_viz = get_vizinhos(vertice, lista_viz.copy(), indice - 1)
    novo_vertice = list(vertice)
    novo_vertice[indice] += 1
    lista_viz = get_vizinhos(tuple(novo_vertice), lista_viz.copy(), indice - 1)
    if novo_vertice[indice] > 1:
        novo_vertice[indice] -= 2
        lista_viz = get_vizinhos(tuple(novo_vertice), lista_viz.copy(), indice - 1)
    return lista_viz

indice = dimensoes - 1 # Indice que sera usado pela funcao que retorna os vizinhos
no_anterior = None

# Calculo da quantidade de expansoes, dos saltos e da media de H dos vizinhos de cada no
for it in iteracao:
    vertice = it[1]
    # Atualiza o numero de expansoes.
    try:
        num_expansoes[vertice] += 1
    except:
        num_expansoes[vertice] = 1
    
    # Obtem os vizinhos do vertice
    vizinhos = get_vizinhos(vertice, [], indice)
    vizinhos = list(dict.fromkeys(vizinhos)) # Retira as repeticoes
    vizinhos.remove(vertice) # A lista de vizinhos tambem inclui o vertice original. Aqui ele eh retirado.

    # Verifica se houve algum salto. Se houve, atualiza o contador e coloca o salto na lista de saltos.
    if no_anterior != None:
        if not (no_anterior in vizinhos):
            num_saltos += 1
            saltos.append((no_anterior, vertice))

    # Calcula a media de H dos vizinhos que foram expandidos
    num_viz = 0 # Quantidade de vizinhos que foram expandidos
    soma = 0
    for vizinho in vizinhos:
        # Se o vizinho nao tiver sido expandido, ele nao estara no dicionario com os valores de h
        try:
            soma += h[vizinho]
        except:
            continue
        
        num_viz += 1 # Atualiza a quantidade de vizinhos expandidos

    # Se o vertice nao tem vizinhos expandidos, a media eh armazenada como -1
    if num_viz == 0:
        med_h_vizinhos[vertice] = -1
    else:
        med_h_vizinhos[vertice] = soma/num_viz
        
    no_anterior = vertice


# Impressao da quantidade de iteracoes:
print(f"Quantidade de iteracoes: {len(iteracao)}\n")

# Impressao dos vertices que foram abertos:
print("Vertices abertos\tNumero de expansoes:")
for it in iteracao:
    print(f"{it[1]}\t{num_expansoes[it[1]]}")
print("\n")

# Impressao dos saltos
print(f"Quantidade de saltos: {num_saltos}")
print("Lista de saltos:")
print(f"Origem\tDestino")
for salto in saltos:
    print(f"{salto[0]}\t{salto[1]}")
print("\n")

# Impressao das medias dos valores de h dos vizinhos:
print("Vertice\tMedia de h dos vizinhos")
for vertice in med_h_vizinhos:
    if med_h_vizinhos[vertice] == -1:
        print(f"{vertice}\tSem vizinhos expandidos")
        continue
    print(f"{vertice}\t{med_h_vizinhos[vertice]}")

# Geracao dos graficos

preteridas = []
# Se houver mais de 3 sequencias alinhadas, o usuario escolhe quais sequencias serao mostradas
if dimensoes > 3:
    while True:
        escolhidas = input("Escolha as 3 dimensoes que serao mostradas, separadas por virgulas.\n").replace(" ", "").split(",")
        if len(escolhidas) != 3:
            continue
        for i in range(3):
            escolhidas[i] = int(escolhidas[i])
        for i in range(dimensoes):
            if not i in escolhidas:
                preteridas.append(i)
        break

    x = [[],[],[],[]]
    y = [[],[],[],[]]
    z = [[],[],[],[]]
    t = [[],[],[],[]]
    pos_subplot = (221,222,223,224)
    while preteridas != []:
        preterida = preteridas.pop()
        while True:
            id_preterida = input(f"Escolha 4 coordenadas para a dimensao {preterida} (comprimento = {len(iteracao)})").replace(" ", "").split(",")
            if len(id_preterida) != 4:
                continue
            for i in range(len(id_preterida)):
                id_preterida[i] = int(id_preterida[i])

            for it in iteracao:
                vertice = it[1]
                if vertice[preterida] == id_preterida[0]:
                    x[0].append(vertice[escolhidas[0]])
                    y[0].append(vertice[escolhidas[1]])
                    z[0].append(vertice[escolhidas[2]])
                    t[0].append(it[0])

                elif vertice[preterida] == id_preterida[1]:
                    x[1].append(vertice[escolhidas[0]])
                    y[1].append(vertice[escolhidas[1]])
                    z[1].append(vertice[escolhidas[2]])
                    t[1].append(it[0])

                elif vertice[preterida] == id_preterida[2]:
                    x[2].append(vertice[escolhidas[0]])
                    y[2].append(vertice[escolhidas[1]])
                    z[2].append(vertice[escolhidas[2]])
                    t[2].append(it[0])

                elif vertice[preterida] == id_preterida[3]:
                    x[3].append(vertice[escolhidas[0]])
                    y[3].append(vertice[escolhidas[1]])
                    z[3].append(vertice[escolhidas[2]])
                    t[3].append(it[0])

            # Loop de criacao dos graficos
            fig = plt.figure()
            for i in range(4):
                ax = fig.add_subplot(pos_subplot[i], projection = '3d')
                ax.title.set_text(f"Dimensao {preterida} = {id_preterida[i]}")
                x_np = np.array(x[i])
                y_np = np.array(y[i])
                z_np = np.array(z[i])
                t_np = np.array(t[i])
                grafico = ax.scatter(x_np, y_np, z_np, c = t_np, cmap = 'viridis', marker = 'o')
                # Coloca linhas
                # for j in range(len(x_np) - 1):
                #     ax.plot([x_np[j], x_np[j+1]], [y_np[j], y_np[j+1]], [z_np[j], z_np[j+1]], linestyle='--', color='black')
                barra = fig.colorbar(grafico)
                barra.set_label('Iteração')

            break
    
# Caso com 3 sequencias alinhadas
else:
    x = []
    y = []
    z = []
    tempo = []
    for it in iteracao:
        x.append(it[1][0])
        y.append(it[1][1])
        z.append(it[1][2])
        tempo.append(it[0])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    # Os vetores x, y e z correspondem as coordenadas dos pontos no grafico.
    # O vetor de tempo determinara a cor de cada ponto.
    grafico = ax.scatter(x,y,z, c = tempo, cmap = 'viridis', marker = 'o')

    # Definicao de limites dos eixos x e y
    ### NAO FUNCIONOU... ###
    # ax.set_xlim(xmin=50, xmax=150)
    # ax.set_ylim(ymin=200, ymax=400)

    # Cria uma barra de cores para ser usada na legenda.
    barra = fig.colorbar(grafico)
    barra.set_label('Iteração')

plt.show()
