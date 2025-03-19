import networkx as nx
import matplotlib.pyplot as plt


def criar_grafo():
    G = nx.Graph()  # Criar um grafo vazio

    vertices= []  # Lista com os vértices	
    rodadas = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11', 'R12', 'R13', 'R14']  # Siglas das rodadas
    times = ['DFC', 'TFC', 'AFC', 'LFC', 'FFC', 'OFC', 'CFC']  # Siglas dos times
    nomes_times = dict()  # Dicionário com os nomes dos times
    jogos = []  # Lista com os jogos
  # Cores para colorir os vértices

    nomes_times['DFC'] = 'Dragões FC'
    nomes_times['TFC'] = 'Tubarões FC'
    nomes_times['AFC'] = 'Águias FC'
    nomes_times['LFC'] = 'Leões FC'
    nomes_times['FFC'] = 'Falcões FC'
    nomes_times['OFC'] = 'Orcas FC'
    nomes_times['CFC'] = 'Crocodilos FC'

    for i in range(0, 7):
        for j in range(0, 7):
            if i != j:
                G.add_node(f"{times[i]}x{times[j]}", cor=None)  # Adicionar 21 arestas
                jogos.append(f"{times[i]}x{times[j]}")
                vertices.append(f"{times[i]}x{times[j]}")

    for i in range(14):  # Adicionar 14 nós das rodadas com cores únicas
        rodada = rodadas[i]
        G.add_node(rodada, cor = None)
        vertices.append(rodadas[i])

    return G, times, jogos, rodadas , vertices

def adicionar_arestas(G, times):
    adicionar_arestas_de_restricoes(G, times)
    adicionar_arestas_entre_jogos_do_mesmo_time(G, times, jogos)
    adicionar_arestas_entre_rodadas(G, rodadas) 


def adicionar_arestas_de_restricoes(G, times): # Adicionar arestas para respeitar as restrições especificadas
    G.add_edge('R1', 'DFCxCFC')
    G.add_edge('R14', 'DFCxCFC')
    G.add_edge('R7', 'LFCxFFC')
    G.add_edge('R13', 'LFCxFFC')
    G.add_edge('R10', 'OFCxLFC')
    G.add_edge('R11', 'OFCxLFC')
    G.add_edge('R12', 'AFCxFFC')
    G.add_edge('R13', 'AFCxFFC')
    G.add_edge('R2', 'CFCxTFC')
    G.add_edge('R3', 'CFCxTFC')

    for i in range(0, 7):  # Adicionar arestas para respeitar a restrição de TFC mandante não com OFC mandante
        if times[i] == 'TFC':
            continue
        for j in range(0, 7):
            if times[j] == 'OFC':
                continue
            G.add_edge(f"TFCx{times[i]}", f"OFCx{times[j]}")

    for i in range(0, 7):  # Adicionar arestas para respeitar a restrição de AFC mandante não com FFC mandante
        if times[i] == 'AFC':
            continue
        for j in range(0, 7):
            if times[j] == 'FFC':
                continue
            G.add_edge(f"AFCx{times[i]}", f"FFCx{times[j]}")


def adicionar_arestas_entre_rodadas(G, rodadas):
    for i in range(0, 14):  # Adicionar arestas entre todas as rodadas
        for j in range(0, 14):
            if i != j:
                G.add_edge(rodadas[i], rodadas[j])


def eh_seguro(G, vertice, cor):
    # Verificar se a cor 'c' é segura para o vértice 'v'
    for neighbor in G.neighbors(vertice):
        if G.nodes[neighbor]['cor'] == cor:
            return False
    return True


def colorir_grafo(G, v, vertices):
    # Caso base: Se todos os vértices estão coloridos, retornar verdadeiro
    if v == len(G.nodes):
        return True
    
    vertice = vertices[v]
    # Tentar diferentes cores para o vértice atual 'v'
    for c in range(0, 14):
        # Verificar se a atribuição da cor 'c' para 'v' é válida
        cor = cores[c]
        if eh_seguro(G, vertice, cor):
            G.nodes[vertice]['cor'] = cor
            # Recursivamente atribuir cores aos restantes vértices
            if colorir_grafo(G, v + 1, vertices):
                return True
            # Se atribuir a cor 'c' não leva a uma solução, removê-la
            G.nodes[vertice]['cor'] = None
    # Se nenhuma cor pode ser atribuída a este vértice, retornar falso
    return False




def agrupa_por_rodada():
    rodadas.sort(key=lambda x: int(x[1:]))
    jogados = []
    for rodada in rodadas:
        print(f"\n{rodada}: com cor: {G.nodes[rodada]['cor']}")
        cor = G.nodes[rodada]['cor']

        for jogo in jogos:
            if G.nodes[jogo]['cor'] == cor:
                print(f"{rodada}: {jogo}")
                jogados.append(jogo)

def adicionar_arestas_entre_jogos_do_mesmo_time(G, times, jogos):
    # Para cada time, encontrar todos os jogos em que ele participa
    for time in times:
        jogos_do_time = []
        for jogo in jogos:
            if time in jogo:  # Verifica se o time é mandante ou visitante no jogo
                jogos_do_time.append(jogo)
        
        # Adicionar arestas entre todos os jogos do mesmo time
        for i in range(len(jogos_do_time)):
            for j in range(i + 1, len(jogos_do_time)):
                G.add_edge(jogos_do_time[i], jogos_do_time[j])




def imprimir_grafo(G): #Imprimir grafo na tela
    pos = nx.circular_layout(G)
    colors = []
    for n in G.nodes:
        if G.nodes[n]['cor'] is not None:
            colors.append(G.nodes[n]['cor'])
        else:
            colors.append('gray')  # Default color for uncolored nodes
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=1500, font_size=8)
    plt.show()


# Execução do código

cores = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'brown', 'cyan', 'magenta', 'lime', 'olive', 'navy','teal']

G, times, jogos, rodadas, vertices = criar_grafo()
adicionar_arestas(G, times)
adicionar_arestas_entre_jogos_do_mesmo_time(G, times, jogos)
adicionar_arestas_entre_rodadas(G, rodadas)


imprimir_grafo(G)

colorir_grafo(G, 0, vertices)

imprimir_grafo(G)
agrupa_por_rodada()


