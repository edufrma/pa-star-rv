# Código adaptado de:
# https://www.mygreatlearning.com/blog/a-search-algorithm-in-artificial-intelligence


def aStarAlgo(start_node, stop_node):

  open_set = set(start_node)
  closed_set = set()
  g = {}  #store distance from starting node
  parents = {}  # parents contains an adjacency map of all nodes
  contagem = {}  # Conta quantas vezes cada vertice foi aberto.
  for vertice in Graph_nodes:
    contagem[vertice] = 0

  #ditance of starting node from itself is zero
  g[start_node] = 0
  #start_node is root node i.e it has no parent nodes
  #so start_node is set to its own parent node
  parents[start_node] = start_node
  iteracao = 0
  saltos = []
  ordem = []
  n = None
  # Armazena a media das estimativas dos vizinhos de cada vertice.
  avg_h = {}
  for vertice in Graph_nodes:
    avg_h[vertice] = 0
    for (vizinho, peso) in get_neighbors(vertice):
      avg_h[vertice] = avg_h[vertice] + heuristic(vizinho)
    avg_h[vertice] = avg_h[vertice] / len(get_neighbors(vertice))
    avg_h[vertice] = round(avg_h[vertice], 2)

  while len(open_set) > 0:
    anterior = n  # Vertice aberto na iteracao anterior
    n = None

    #node with lowest f() is found
    for v in open_set:
      if n == None or g[v] + heuristic(v) < g[n] + heuristic(n):
        n = v

    ordem.append(n)
    if anterior != None:
      mudou = True
      for (vizinho, peso) in get_neighbors(anterior):
        if vizinho == n:
          mudou = False
          break

      if mudou:
        saltos.append((anterior, n))
        print(f"Salto de {anterior} para {n}.")

    contagem[n] = contagem[n] + 1
    print(f"Iteracao {iteracao}")
    print("Conjunto aberto:")
    print(f"\t{open_set}")
    print("Conjunto fechado:")
    print(f"\t{closed_set}")
    print(f"Vertice escolhido: {n}\n")

    if n == stop_node or Graph_nodes[n] == None:
      pass
    else:
      for (m, weight) in get_neighbors(n):
        #nodes 'm' not in first and last set are added to first
        #n is set its parent
        if m not in open_set and m not in closed_set:
          open_set.add(m)
          parents[m] = n
          g[m] = g[n] + weight

        #for each node m,compare its distance from start i.e g(m) to the
        #from start through n node
        else:
          if g[m] > g[n] + weight:
            #update g(m)
            g[m] = g[n] + weight
            #change parent of m to n
            parents[m] = n

            #if m in closed set,remove and add to open
            if m in closed_set:
              closed_set.remove(m)
              open_set.add(m)

    if n == None:
      print('Path does not exist!')
      print(contagem)
      print(len(saltos))
      print(saltos)
      print(avg_h)
      return None

    # if the current node is the stop_node
    # then we begin reconstructin the path from it to the start_node
    if n == stop_node:
      path = []

      while parents[n] != n:
        path.append(n)
        n = parents[n]

      path.append(start_node)

      path.reverse()

      print('Path found: {}'.format(path))
      print("Contagem:")
      print(contagem)
      print("Saltos:")
      print(len(saltos))
      print(saltos)
      print("Media das heuristicas vizinhas:")
      print(avg_h)
      print("Ordem de analise:")
      print(ordem)
      return path

    # remove n from the open_list, and add it to closed_list
    # because all of his neighbors were inspected
    open_set.remove(n)
    closed_set.add(n)
    iteracao = iteracao + 1

  print('Path does not exist!')
  print(contagem)
  return None


#define fuction to return neighbor and its distance
#from the passed node
def get_neighbors(v):
  if v in Graph_nodes:
    return Graph_nodes[v]
  else:
    return None


# Escolha do grafo
print("Escolha o grafo a ser usado:")
print("1 - www.mygreatlearning.com")
print("2 - optimization.cbe.cornell.edu")
print("3 - dtai.cs.kuleuven.be - pag. 15")
print("4 - www.gatevidyalay.com/ - problema 2")
escolha = input()

if (escolha == '1'):
  #for simplicity we ll consider heuristic distances given
  #and this function returns heuristic distance for all nodes
  def heuristic(n):
    H_dist = {
        'A': 11,
        'B': 6,
        'C': 99,
        'D': 1,
        'E': 7,
        'G': 0,
    }

    return H_dist[n]

  #Describe your graph here

  Graph_nodes = {
      'A': [('B', 2), ('E', 3)],
      'B': [('A', 2), ('C', 1), ('G', 9)],
      'C': [('B', 1)],
      'E': [('A', 3), ('D', 6)],
      'D': [('E', 6), ('G', 1)],
      'G': [('B', 9), ('D', 1)]
  }
  aStarAlgo('A', 'G')

# Exemplo de https://optimization.cbe.cornell.edu/index.php?title=A-star_algorithm#Numerical_Example
elif (escolha == '2'):

  Graph_nodes = {
      'A': [('B', 18.4), ('C', 12.7)],
      'B': [('A', 18.4), ('C', 14.1)],
      'C': [('A', 12.7), ('B', 14.1), ('D', 14.4), ('H', 14.8)],
      'D': [('C', 14.4), ('E', 8.8)],
      'E': [('D', 8.8), ('F', 10.9), ('G', 18.9)],
      'F': [('E', 10.9), ('G', 10.7), ('H', 12.0)],
      'G': [('E', 18.9), ('F', 10.7), ('I', 15.5), ('K', 21.0)],
      'H': [('C', 14.8), ('F', 12.0), ('I', 11.3), ('J', 17.6)],
      'I': [('G', 15.5), ('H', 11.3), ('K', 12.4)],
      'J': [('H', 17.6), ('K', 17.5)],
      'K': [('G', 21.0), ('I', 12.4), ('J', 17.5)]
  }

  def heuristic(n):
    H_dist = {
        'A': 57.2,
        'B': 46.3,
        'C': 40.8,
        'D': 52.7,
        'E': 42.2,
        'F': 30.1,
        'G': 21.0,
        'H': 26.8,
        'I': 12.4,
        'J': 18.1,
        'K': 0.0
    }

    return H_dist[n]

  aStarAlgo('A', 'K')

# Exemplo de https://dtai.cs.kuleuven.be/education/ai/Exercises/Session2/Solutions/solution.pdf
# pagina 15

elif (escolha == '3'):
  Graph_nodes = {
      'S': [('A', 6), ('B', 5), ('C', 10)],
      'A': [('S', 6), ('E', 6)],
      'B': [('S', 5), ('D', 7), ('E', 6)],
      'C': [('S', 10), ('D', 6)],
      'D': [('B', 7), ('C', 6), ('F', 6)],
      'E': [('A', 6), ('B', 6), ('F', 4)],
      'F': [('D', 6), ('E', 4), ('G', 3)],
      'G': [('F', 3)]
  }

  def heuristic(n):
    H_dist = {
        'S': 17,
        'A': 10,
        'B': 13,
        'C': 4,
        'D': 2,
        'E': 4,
        'F': 1,
        'G': 0
    }

    return H_dist[n]

  aStarAlgo('S', 'G')

# Problema 2 de https://www.gatevidyalay.com/a-algorithm-a-algorithm-example-in-ai/
elif (escolha == '4'):
  Graph_nodes = {
      'A': [('B', 6), ('F', 3)],
      'B': [('A', 6), ('C', 3), ('D', 2)],
      'C': [('B', 3), ('D', 1), ('E', 5)],
      'D': [('B', 2), ('C', 1), ('E', 8)],
      'E': [('C', 5), ('D', 8), ('I', 5), ('J', 5)],
      'F': [('A', 3), ('G', 1), ('H', 7)],
      'G': [('F', 1), ('I', 3)],
      'H': [('F', 7), ('I', 2)],
      'I': [('E', 5), ('G', 3), ('H', 2), ('J', 3)],
      'J': [('E', 5), ('I', 3)]
  }

  def heuristic(n):
    H_dist = {
        'A': 10,
        'B': 8,
        'C': 5,
        'D': 7,
        'E': 3,
        'F': 6,
        'G': 5,
        'H': 3,
        'I': 1,
        'J': 0
    }

    return H_dist[n]

  aStarAlgo('A', 'J')
