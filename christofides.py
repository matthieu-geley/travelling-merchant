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
1. On calcule l'arbre couvrant minimal (MST)
2. On trouve les sommets de degrés impair dans le MST
3. On fait un couplage parfait minimum sur les sommets impairs
4. On ajoute les arêtes du couplage au MST afin de créer un graphe Eulérien
5. On cherche à trouver un circuit Eulérien
6. On convertit ça en une tournée Hamiltonienne pour éviter les répétitions
7. On finit par retourner le chemin trouvé.
"""
def christofides(villes):
    G = create_complete_graph(villes)
    mst = nx.minimum_spanning_tree(G)

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
