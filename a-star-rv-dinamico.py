# Resolucao do problema 1 encontrado em
# https://www.gatevidyalay.com/a-algorithm-a-algorithm-example-in-ai/

# Cada vertice eh representado por uma tupla de tuplas que forma uma matriz 3 x 3.
# O espaco vazio eh representado por 0.

inic = ((2, 8, 3), (1, 6, 4), (7, 0, 5))
fim = (
    (1, 2, 3), (8, 0, 4), (7, 6, 5))  # Proposto pelo problema 1. 6 iteracoes.
#fim = ((0, 1, 4), (2, 8, 3), (7, 6, 5))  # 2658 iteracoes
#fim = ((3, 2, 1), (7, 0, 5), (4, 6, 8))  # 5277 iteracoes

interv = 1  #Intervalo de iterações registradas nos arquivos.

num_verts = 362880  # Quantidade de nos no grafo (9!).


# Retorna o valor de h de um vertice.
def get_h(vertice, obj):
  h = 0
  for i in range(3):
    for j in range(3):
      if vertice[i][j] != 0 and vertice[i][j] != obj[i][j]:
        h = h + 1
  return h


def fPrintDict(dict, arq):
  for chave in dict:
    arq.write(f"{chave} : {dict[chave]}\n")
  return


def fPrintSet(conjunto, arq):
  for elemento in conjunto:
    arq.write(f"{elemento}\n")
  return


def fPrintSetGH(conjunto, arq, g, h):
  for elemento in conjunto:
    arq.write(f"{elemento}\t g = {g[elemento]}\th = {h[elemento]}\n")
  return


# Retorna as coordenadas do espaco vazio de um vertice
def get_zero(vertice):
  for i in range(3):
    for j in range(3):
      if vertice[i][j] == 0:
        return (i, j)
  return None


# Verifica se um vertice esta no formato certo (matriz 3 x 3 com numeros de 0 a 8 nao repetidos).
def check_vert(vert):
  if len(vert) != 3:
    return False
  elementos = set(range(9))
  for linha in vert:
    if (len(vert)) != 3:
      return False
    for num in linha:
      if num not in elementos:
        return False
      elementos.remove(num)
  return True


# Funcao que retorna os vizinhos de um vertice.
# Recebe um vertice e as coordenadas de seu espaco vazio.
def getNeighbors(vertice, x, y):
  vizinhos = []
  vert = list(vertice)
  for i in range(3):
    vert[i] = list(vert[i])

  if (x > 0):
    viz = []
    for i in range(3):
      viz.append(vert[i].copy())
    viz[x][y] = viz[x - 1][y]
    viz[x - 1][y] = 0

    for i in range(3):
      viz[i] = tuple(viz[i])
    viz = tuple(viz)

    vizinhos.append((viz, x - 1, y))

  if (x < 2):
    viz = []
    for i in range(3):
      viz.append(vert[i].copy())
    viz[x][y] = viz[x + 1][y]
    viz[x + 1][y] = 0

    for i in range(3):
      viz[i] = tuple(viz[i])
    viz = tuple(viz)

    vizinhos.append((viz, x + 1, y))

  if (y > 0):
    viz = []
    for i in range(3):
      viz.append(vert[i].copy())
    viz[x][y] = viz[x][y - 1]
    viz[x][y - 1] = 0

    for i in range(3):
      viz[i] = tuple(viz[i])
    viz = tuple(viz)

    vizinhos.append((viz, x, y - 1))

  if (y < 2):
    viz = []
    for i in range(3):
      viz.append(vert[i].copy())
    viz[x][y] = viz[x][y + 1]
    viz[x][y + 1] = 0

    for i in range(3):
      viz[i] = tuple(viz[i])
    viz = tuple(viz)

    vizinhos.append((viz, x, y + 1))

  return vizinhos


def aStarProg(inic, fim, intervalo):
  # Verifica se os vertices de inicio e de fim estao corretos.
  if not check_vert(inic):
    print("Vertice inicial em formato errado.")
    return

  if not check_vert(fim):
    print("Vertice final em formato errado.")
    return

  if (intervalo < 0 or type(intervalo) != int):
    print("Intervalo invalido.")
    return

  contador = 0  # Contador de vertices. Nao inclui o vertice inicial.
  expandidos = 0  # Contador de vertices expandidos.
  vertices = {inic}  # Conjunto dos vertices.
  zeros = {
      inic: get_zero(inic)
  }  # Registra a localizacao do espaco vazio de cada vertice
  g = {inic: 0}  # Guarda os valores de g para cada vertice
  h = {inic: get_h(inic, fim)}  # Guarda os valores de h para cada vertice
  antecessores = {
      inic: None
  }  # Guarda os antecessores de cada vertice. O vertice inicial nao tem antecessores.

  # guarda quantas vezes cada vertice foi aberto
  contagem = {inic: 0}

  aberto = {inic}
  fechado = set()
  # Diz qual a iteração atual
  iteracao = 0

  viz_anteriores = [inic]
  anterior = inic
  saltos = set()
  ordem = []

  arq = open("./iteracoes.txt", "w")  # Abre o arquivo de iteracoes

  # Comeca a varredura
  while len(aberto) > 0:
    iteracao = iteracao + 1
    # Escolhe o vertice do conjunto aberto com o menor valor de f.
    vert = None
    fmin = None

    for v in aberto:
      f = g[v] + h[v]
      if vert == None or (f < fmin):
        vert = v
        fmin = f

    # Escreve no arquivo de iteracoes
    if (intervalo != 0 and iteracao % intervalo == 0):
      arq.write(f"Iteracao {iteracao}\n")
      arq.write(f"Conjunto aberto ({len(aberto)} elementos):\n")
      fPrintSetGH(aberto, arq, g, h)
      arq.write(f"\nConjunto fechado ({len(fechado)} elementos):\n")
      fPrintSet(fechado, arq)
      arq.write(f"\nVertice escolhido: {vert}\n")
      arq.write("\n")

    # Se o vertice foi expandido pela primeira vez, incrementa o contador de vertices expandidos.
    if contagem[vert] == 0:
      expandidos += 1
    contagem[vert] += 1
    if vert not in viz_anteriores:
      saltos.add((anterior, vert))

    viz_anteriores = []
    anterior = vert
    ordem.append(vert)

    # Encontrado o indice do vertice, ele eh retirado do conjunto aberto e colocado no conjunto fechado.
    aberto.remove(vert)
    fechado.add(vert)

    x0, y0 = zeros[vert]

    # Verifica se o conjunto encontrado eh o vertice final. Se for, imprime o caminho e encerra o programa.
    if vert == fim:
      caminho = [vert]
      vert = antecessores[vert]
      print(f"{iteracao} iteracoes.")
      arq.close()
      arq = open("./dados.txt", "w")
      # Escreve a quantidade de vertices revelados
      arq.write(f"{len(vertices)} vertices na lista open.\n")
      arq.write(f"{(len(vertices)*100.0/num_verts):.2f} % do total.\n")
      # Escreve a quantidade de vertices expandidos
      arq.write(f"\n{expandidos} vertices expandidos.\n")
      arq.write(f"{(expandidos*100.0/num_verts):.2f} % do total.\n")
      while (vert != None):
        caminho.append(vert)
        vert = antecessores[vert]

      arq.write(f"\n{iteracao} iteracoes.\n")
      arq.write("Caminho encontrado:\n")
      for vert in reversed(caminho):
        arq.write(str(vert) + "\n")
      arq.write("\n")

      arq.write("Contagem:\n")
      fPrintDict(contagem, arq)

      arq.write(f"\nSaltos: {len(saltos)}\n")
      fPrintSet(saltos, arq)

      arq.write(f"\nOrdem de analise:\n")
      fPrintSet(ordem, arq)

      arq.write(f"\nMedia das distancias estimadas dos vizinhos:\n")
      for vertice in vertices:
        media = 0
        x, y = zeros[vertice]
        vizinhos = getNeighbors(vertice, x, y)
        for (vizinho, x0, y0) in vizinhos:
          media += get_h(vizinho, fim)
        media = media / len(vizinhos)
        arq.write(f"{vertice} : {media:.2f}\n")

      arq.close()

      print("Caminho encontrado. Ver arquivos.")
      return

    # Varredura dos vizinhos do vertice.
    for (vizinho, x0, y0) in getNeighbors(vert, x0, y0):
      viz_anteriores.append(vizinho)
      # Verifica se o vizinho ja foi visitado anteriormente
      if vizinho in vertices:
        # Se o vizinho ja foi visitado, ele estara ou no conjunto aberto ou no fechado.
        # Neste caso, so havera mudancas se o valor de f do vertice for menor do que o armazenado.
        # Como o valor de h de cada vertice eh imutavel, basta verificar se houve mudanca em g.
        g_atual = g[vert] + 1
        if g_atual < g[vizinho]:
          g[vizinho] = g_atual
          antecessores[vizinho] = vert

          # Se o vertice esta no conjunto fechado, ele volta para o aberto.
          if vizinho in fechado:
            fechado.remove(vizinho)
            aberto.add(vizinho)

      # Se o vizinho nunca foi explorado, seus dados sao preenchidos e ele eh colocado no conjunto aberto.
      else:
        contador = contador + 1
        vertices.add(vizinho)
        zeros[vizinho] = (x0, y0)
        g[vizinho] = g[vert] + 1
        h[vizinho] = get_h(vizinho, fim)
        antecessores[vizinho] = vert
        contagem[vizinho] = 0

        aberto.add(vizinho)

  print("Nenhum caminho encontrado")
  arq.close()


aStarProg(inic, fim, interv)
