# travelling-merchant

## 1. Introduction  
Ce projet nous plonge dans l'un des problèmes classiques de l'optimisation : le problème du Voyageur de Commerce (TSP). À travers sa résolution, nous serons amenés à développer des compétences variées en algorithmique, mathématiques appliquées et programmation. Plus précisément, ce projet mettra en lumière des méthodes pour résoudre des problèmes NP-difficiles, qui nécessitent souvent l'emploi d'approches heuristiques ou approximatives, en raison de la complexité croissante des solutions exactes.

Au-delà de la simple implémentation algorithmique, la résolution du TSP dans un contexte pratique nous permettra de manipuler des concepts d'algorithmes combinatoires, comme l'algorithme de Christofides, tout en explorant des approches évolutives comme les algorithmes génétiques. Ce projet favorisera ainsi une approche rigoureuse et scientifique de la résolution de problèmes, tout en développant des compétences en analyse de performance et en comparaison des solutions proposées.

En outre, ce projet constituera une expérience enrichissante pour quiconque cherche à maîtriser des outils fondamentaux dans le domaine de l'optimisation et de la recherche opérationnelle, des compétences particulièrement recherchées dans le monde de la data science et de l’intelligence artificielle.

## 2. Présentation du projet
_Description du projet:_  

"Dans la France médiévale, les routes sinueuses et dangereuses, les forêts épaisses, et les montagnes escarpées constituaient des défis quotidiens pour les voyageurs. Les marchands ambulants jouaient un rôle crucial dans l'économie en transportant des marchandises (souvent) rares et précieuses d'une contrée à l'autre. Ces marchands devaient parcourir de
longues distances pour vendre leurs biens dans différents marchés et foires.  

Théobald est un marchand expérimenté dont le succès dépend de sa capacité à planifier efficacement ses voyages pour maximiser ses profits et minimiser les risques inhérents à chaque trajet. En effet, chaque détour inutile ou route imprévue peut entraîner des coûts supplémentaires, des retards, et une exposition accrue aux dangers comme les bandits et les conditions météorologiques imprévisibles. C'est ici qu'intervient le Problème du Voyageur de Commerce (TSP), un défi mathématique et algorithmique consistant à trouver le chemin le plus court permettant de visiter un ensemble donné de villes une seule fois avant de revenir au point de départ. Dans le contexte de Théobald, la résolution optimale de ce problème est cruciale pour la viabilité économique de ses voyages. Le TSP est reconnu comme un problème NP-difficile, ce qui signifie qu'il n'existe pas de solution efficace connue pour toutes les instances du problème.  

Malgré cela, diverses méthodes et heuristiques permettent de trouver des solutions approximatives ou exactes dans des délais raisonnables. Toujours désireux d’aider votre prochain, vous prenez pitié de votre marchand ambulant préféré et vous lui donnez la chance de voyager sur des sentiers sécurisés. Votre objectif est d’identifier le chemin le plus court parmi les (n-1)! chemins possibles (où n est le nombre de villes à visiter) et ça bien sûr sans tous les évaluer !"  

_Réalisation du projet_  
Pour ce projet nous avons travaillé à trois en suivant le plan suivant: 
- 1) Modélisation du problème
- 2) Résolution avec l'algorithme de Christofides
- 3) Résolution avec les algorithmes génétiques
- 4) Analyse comparative
- 5) Conclusion  

C'est ce même plan que vous retrouverez dans ce Readme.  
Chacun d'entre nous avait une tâche à réaliser et nous nous sommes servis de Github pour le versionning de notre projet.  

_Architecture du projet:_  
Dans ce repository Github vous retrouverez trois fichiers pythons: 
- christofides.py dans lequel vous retrouverez la logique qui implémente l'algorithme de Christofides  
- genetic.py dans lequel vous retrouverez la logique qui implémente des algorithmes génétiques  
- main.py qui est notre point d'entrée et d'exécution de nos scripts.  

## 3. Algorithme de Christofides
### 3.1 Introduction  
L'algorithme de Christofides est une méthode d'approximation efficace pour résoudre le problème du voyageur de commerce (TSP), notamment dans des cas où obtenir une solution exacte serait trop coûteux en termes de calcul. Cet algorithme garantit une solution approchée dont la longueur ne dépasse jamais 1,5 fois la longueur de la solution optimale. Il est particulièrement adapté dans le cadre du TSP, car il permet de trouver un itinéraire court tout en optimisant le temps de calcul, ce qui le rend pertinent pour le projet de cartographie des villes.  

### 3.2 Étapes de l'algorithme  

_a) Génération du graphe complet_  
L'algorithme commence par la création d'un graphe complet. Chaque ville est représentée par un sommet et chaque paire de villes est reliée par une arête pondérée selon la distance qui les sépare.
Cette étape établit la base de travail pour la suite de l'algorithme.  

_b) Calcul du Minimum Spanning Tree (MST)_  
Ensuite, un arbre couvrant minimum (MST) est calculé à partir du graphe complet. Cet arbre est un sous-ensemble d'arêtes connectant tous les sommets du graphe sans former de cycles, et minimise la somme totale des distances des arêtes.
Le MST est utilisé comme une première approximation de l'itinéraire optimal, car il connecte toutes les villes avec le coût minimal.  

_c) Identification des sommets de degré impair_  
Après la construction du MST, les sommets ayant un degré impair (nombre impair de connexions) sont identifiés. Ces sommets doivent être appariés pour que le graphe puisse être transformé en un circuit Eulerien dans la prochaine étape.  

_d) Appariement des sommets impairs_  
Les sommets impairs identifiés sont appariés par un algorithme de couplage parfait, en minimisant la somme des distances des arêtes entre eux. Cet appariement permet de rétablir un degré pair pour tous les sommets concernés, ce qui est nécessaire pour construire un circuit Eulerien.  

_e) Construction du circuit Eulerien_  
Une fois les sommets impairs appariés, le graphe résultant permet de construire un circuit Eulerien. Un circuit Eulerien est un chemin qui passe par chaque arête du graphe exactement une fois.
Cette étape prépare l'algorithme à créer une approximation de la solution du TSP.  

_f) Approximation du circuit Hamiltonien_  
Le circuit Eulerien est ensuite transformé en circuit Hamiltonien, qui est un chemin passant par chaque sommet exactement une fois. Cela se fait en supprimant les doublons de sommets dans l’ordre de passage du circuit Eulerien.
Le résultat est une solution approchée du TSP.  

### 3.3 Pertinence de l'algorithme  

_a) Garantie d'approximation_  
L'algorithme de Christofides garantit que la longueur de la solution trouvée est au maximum 1,5 fois celle du chemin optimal. Cela permet d’obtenir une solution de qualité, proche de l'optimum, tout en évitant la complexité d'une solution exacte.  

_b) Efficacité computationnelle_  
Cet algorithme est plus rapide et plus efficace que les méthodes exactes du TSP, en particulier pour des problèmes de taille moyenne à grande. Cela le rend adapté aux situations où le calcul d'une solution optimale est trop coûteux.  

_c) Contexte de cartographie et d'itinéraires_  
Dans le cadre de la cartographie des villes pour Théobald, l'algorithme de Christofides fournit une solution quasi optimale permettant de minimiser les détours tout en réduisant les risques liés à des trajets prolongés. Il est particulièrement pertinent lorsqu'il s'agit de planifier des itinéraires en fonction des distances entre villes.  

### 3.4 Exécution & Résultats
Lors de l'exécution de l'algorithme, une liste des distances entre les 20 villes s'affiche dans le terminal. En suite, via Pyplot, une fenêtre s'ouvre avec les villes, les routes qui les relient et les distances qui sont placées sur la carte de France.  

![Carte de la France avec les villes, routes et distances](./Docs/img/first_map.png "Carte de la France avec les villes, routes et distances")  

Puis, en suivant les étapes vues dans la partie 3 de ce Readme, l'algorithme de Christofides est appliqué et une autre fenêtre Pyplot s'ouvre avec le meilleur itinéraires pour Théobald.  

![Carte de la France avec le meilleur itinéraire](./Docs/img/best_path_map.png "Carte de la France avec le meilleur itinéraire")  

### 3.5 Conclusion
L'algorithme de Christofides est une solution efficace et presque optimale pour résoudre le TSP dans un contexte de cartographie, où il est crucial de minimiser les distances parcourues tout en maintenant un temps de calcul raisonnable. Sa combinaison de précision et de rapidité en fait un choix pertinent pour des applications telles que la planification des itinéraires commerciaux de Théobald.  

## 4. Algorithme génétique

## 5. Analyse comparative

## 6. Conclusion