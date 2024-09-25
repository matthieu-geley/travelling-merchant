import networkx as nx
from itertools import combinations
from math import sqrt



""" 
Dans un premier temps on calcule la distance Euclidienne entre deux points.
"""
def calcul_distance(ville1, ville2):
    return sqrt((ville1[0] - ville2[0])**2 + (ville1[1] - ville2[1])**2)

""" 
Puis, on crée un graphe complet avec les distances entre chaque paire de villes
"""
def create_complete_graph(villes):
    G = nx.Graph()
    for (ville1, pos1), (ville2, pos2) in combinations(villes.items(), 2):
        distance = calcul_distance(pos1, pos2)
        G.add_edge(ville1, ville2, weight=distance)
    return G

"""
On implémente l'algorithme de Christofides, voici les étapes:
1. On calcule l'arbre couvrant minimal (MST) MST = sous ensemble des arêtes du graphe qui relie toutes les villes avec un cout total minimum
2. On trouve les sommets de degrés impair dans le MST (qui sont connectés a un nombre impair d'arêtes dans l'arbre couvrnat)
3. On fait un couplage parfait minimum sur les sommets impairs (trouver des paires de sommets pour que la somme des distances des arêtes 
connectant ces paires soit minimisée)
4. On ajoute les arêtes du couplage au MST afin de créer un graphe Eulérien (chaque commet a un degrés pair)
5. On cherche à trouver un circuit Eulérien (qui passe par chaque arête une seule fois)
6. On convertit ça en une tournée Hamiltonienne pour éviter les répétitions (passe par une ville une seule fois)
7. On finit par retourner le chemin trouvé.
"""
def christofides(villes):
    G = create_complete_graph(villes)
    mst = create_mst_graph_manual(G)

    odd_nodes = [node for node in mst.nodes() if mst.degree(node) % 2 == 1]

    odd_subgraph = G.subgraph(odd_nodes)
    matching = nx.algorithms.matching.min_weight_matching(odd_subgraph)


    multigraph = nx.MultiGraph(mst)
    multigraph.add_edges_from(matching)

    eulerian_circuit = list(nx.eulerian_circuit(multigraph))

    visited = set()
    hamiltonian_path = []
    for u, v in eulerian_circuit:
        if u not in visited:
            visited.add(u)
            hamiltonian_path.append(u)

    return hamiltonian_path


def prim_mst_manual(F):
# 1. Initialisation
    start_node = list(F.nodes())[0] # Sélection d'un noeud de départ.

    in_mst = set([start_node]) # Contient les noeuds déjà inclus dans le MST. On commence avec le noeud de départ.

    mst_edges = [] # Stocke les arêtes qui font partie du MST

# 2. Boucle principale. Elle continue tant que tous les noeuds ne sont pas inclus dans le MST. On veut un arbre qui couvre tous les noeuds.
    while len(in_mst) < len(F.nodes()):
        min_edge = None
        min_weight = float('inf')
# Pour chaque noeud (u) déjà inclus dans le MST, on regarde ses voisins (v) dans 'F[u].items()'
# On sélectionne l'arête avec le poids le plus faible qui connecte un noeud à l'intérieur du MST avec un noeud à l'extérieur
# On garde la plus petite arête (min_edge) puis on l'ajoute à 'mst_edges' et on inclut 'v' dans le MST (in_mst)
        for u in in_mst:
            for v, data in F[u].items():
                if v not in in_mst and data['weight'] < min_weight:
                    min_weight = data['weight']
                    min_edge = (u, v, min_weight)
# 3. Retour. A la fin de la boucle, tous les noeuds sont connectés et les arêtes minimales sont dans 'mst_edges'
        if min_edge:
            u, v, weight = min_edge
            mst_edges.append((u, v, weight))
            in_mst.add(v)

    return mst_edges

# 4. Construction du graph
def create_mst_graph_manual(F):
    mst_edges = prim_mst_manual(F)
    mst_graph = nx.Graph()

    for u, v, weight in mst_edges:
        mst_graph.add_edge(u, v, weight = weight)
    return mst_graph