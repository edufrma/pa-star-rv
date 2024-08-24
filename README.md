Este repositório contém os códigos usados no trabalho de graduação "A-Star-RV e PA-Star-RV: Visualização da Execução das Ferramentas de Busca A-Star e PA-Star", de Eduardo Freire Martins, sob orientação da Prof.ª Dr.ª Alba Cristina Magalhães Alves de Melo (Universidade de Brasília, Depto. de Ciência da Computação).

# Descrição dos Arquivos

- O diretório astar_msa contém a ferramenta PA-Star, disponível [neste repositório](https://github.com/danielsundfeld/astar_msa), modificada para incluir um contador atômico de iterações e para imprimir as iterações e o _thread_ de execução no _log_ de saída.
- Os arquivos _a-star-rv-estatico.py_ e _a-star-rv-dinamico.py_ contém duas implementações do A-Star-Rv usadas neste trabalho: a primeira para analisar grafos estáticos e a segunda para grafos dinâmicos.
- O arquivo _pa-Star-rv.py_ contém a maior parte da implementação da ferramenta PA-Star-RV. Ele recebe os _logs_ de saída do PA-Star, imprime as métricas e mostra o gráfico que mostra os nós expandidos por iteração.
- Por fim, o arquivo _it-f.py_ é responsável por imprimir o gráfico que mostra o valor de f escolhido em cada iteração. Para tanto, ele deve receber a localização de um diretório com 4 arquivos de _log_ de saída com os nomes _log1.txt_, _log2.txt_, _log4.txt_ e _log8.txt_ que correspondem, respectivamente, aos _logs_ das análises feitas com 1, 2, 4 e 8 _threads_. Caso o usuário queira, ele pode passar via linha de comando mais dois argumentos numéricos que corresponderão, respectivamente, aos valores mínimo e máximo do eixo y dos gráficos gerados.
