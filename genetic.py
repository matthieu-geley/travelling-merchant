import random
from math import radians, sin, cos, sqrt, atan2
import matplotlib.pyplot as plt
import networkx as nx

class AlgorithmeGenetiqueTSP:
    def __init__(self, population_size, selection_type, reproduction_type, mutation_rate, generations):
    
        self.population_size = population_size          # Taille de la population
        self.selection_type = selection_type   
        self.reproduction_type = reproduction_type      # Système de croisement
        self.mutation_rate = mutation_rate              # Taux de mutation
        self.generations = generations                  # Nombre de générations
        self.population = []                            # La population d'individus (chemins)

    def create_random_ways(self, df):
        # Extraire les noms de villes en tant que liste
        villes = df['Ville'].tolist()
        ways = [] 
        for _ in range(self.population_size):
            way = villes.copy()  # Faire une copie de la liste de villes
            random.shuffle(way)  # Mélanger les villes
            ways.append(way)
        return ways
    
    def initiate_population(self, cities):
    # On ajoute les chemins à la population
        self.population = self.create_random_ways(cities)
        if len(self.population) < self.population_size:
            raise ValueError(f"Population trop petite. Taille actuelle: {len(self.population)}")

    # Calculer la distance entre deux villes 
    def haversine(self,lon1, lat1, lon2, lat2):
        R = 6371.0  # Rayon de la Terre en km

        # On convertit les degrés en radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # On calcule la différence des coordonnées
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        # Formule de Haversine
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # Distance en kilomètres
        distance = R * c
        return distance
    def precalculate_distances(self, df):
        distances = {}
        villes = df['Ville'].tolist()  # Liste des villes
        
        # Boucle pour précalculer les distances entre chaque paire de villes
        for i, ville1 in enumerate(villes):
            for j, ville2 in enumerate(villes):
                if i != j:
                    lat1, lon1 = df.loc[df['Ville'] == ville1, ['Latitude', 'Longitude']].values[0]
                    lat2, lon2 = df.loc[df['Ville'] == ville2, ['Latitude', 'Longitude']].values[0]
                    distance = self.haversine(lon1, lat1, lon2, lat2)
                    
                    # Ajouter les distances dans les deux sens
                    distances[(ville1, ville2)] = distance
                    distances[(ville2, ville1)] = distance
        
        return distances


    def calculate_distance(self, way, distances):
        distance = 0
        # On parcourt chaque paire de villes dans le chemin
        for i in range(len(way) - 1):
            city1 = way[i]
            city2 = way[i + 1]
            distance += distances[(city1, city2)]  # Utilisation des distances précalculées
            # Ajouter la distance du dernier point au point de départ
        distance += distances[(way[-1], way[0])]
        return distance


    def fitness(self, way, distances, cached_fitnesses):
        # Si la fitness de ce chemin est déjà dans le cache, on la retourne
        if tuple(way) in cached_fitnesses:
            return cached_fitnesses[tuple(way)]
        
        # Sinon, on calcule la distance et la fitness
        distance = self.calculate_distance(way, distances)
        fitness_value = 1 / distance
        cached_fitnesses[tuple(way)] = fitness_value  # On ajoute la fitness dans le cache
        
        return fitness_value

    
    def selection_type_selection(self, population, fitnesses):
        if self.selection_type == 'roulette_wheel':
            # Sélectionner deux parents
            return random.sample(self.roulette_wheel_selection(population, fitnesses), 2)
        elif self.selection_type == 'tournament':
            tournament_size = 3  # Choisir la taille du tournoi
            # Sélectionner deux parents
            return random.sample(self.tournament_selection(population, fitnesses, tournament_size), 2)
        elif self.selection_type == 'rank':
            # Sélectionner deux parents
            return random.sample(self.rank_selection(population, fitnesses), 2)


    def tournament_selection(self, population, fitnesses, tournament_size):
        if len(population) < tournament_size:
            raise ValueError(f"La population ({len(population)}) est plus petite que la taille du tournoi ({tournament_size})")
        selected = []
        # On ajuste la taille du tournoi si la population est plus petite
        actual_tournament_size = min(tournament_size, len(population))

        for _ in range(len(population)):
            # On sélectionne un échantillon aléatoire de 'actual_tournament_size' individus
            tournament = random.sample(list(zip(population, fitnesses)), actual_tournament_size)
            # On sélectionne le gagnant avec la meilleure fitness
            winner = max(tournament, key=lambda x: x[1])[0]
            selected.append(winner)

        return selected

    
    def rank_selection(self, population, fitnesses):
        ranks = sorted(range(len(fitnesses)), key=lambda x: fitnesses[x])
        probabilities = [r / len(ranks) for r in ranks]
        selected = []
        for _ in range(len(population)):
            selected.append(random.choices(population, probabilities)[0])
        return selected
    
    def roulette_wheel_selection(self, population, fitnesses):
        total_fitness = sum(fitnesses)
        probabilities = [f / total_fitness for f in fitnesses]
        selected = []
        for _ in range(len(population)):
            selected.append(random.choices(population, probabilities)[0])
        return selected
    
    def crossover(self, parent1, parent2):
        if self.reproduction_type == 'order':
            return self.order_crossover(parent1, parent2)
        elif self.reproduction_type == 'pmx':
            return self.pmx_crossover(parent1, parent2)
        
    def order_crossover(self, parent1, parent2):
        child = [-1] * len(parent1)
        start, end = sorted(random.sample(range(len(parent1)), 2))
        
        # Copier la sous-séquence de parent1 dans l'enfant
        child[start:end] = parent1[start:end]

        # Remplir les positions vides avec les éléments de parent2
        remaining = [x for x in parent2 if x not in child]
        current_pos = 0

        for i in range(start):
            child[i] = remaining[current_pos]
            current_pos += 1

        for i in range(end, len(parent1)):
            child[i] = remaining[current_pos]
            current_pos += 1

        child = self.remove_duplicates(child, parent1)

        return child

    
    def pmx_crossover(self, parent1, parent2):
        child = [-1] * len(parent1)
        start, end = sorted(random.sample(range(len(parent1)), 2))

        # Copier la sous-séquence de parent1 dans l'enfant
        child[start:end] = parent1[start:end]

        # PMX - remplir les parties restantes en respectant la correspondance
        for i in range(start, end):
            if parent2[i] not in child:
                j = i
                # Trouver la bonne position dans parent2
                while parent1[j] in child:
                    j = parent2.index(parent1[j])
                child[j] = parent2[i]

        for i in range(len(child)):
            if child[i] == -1:
                child[i] = parent2[i]

        child = self.remove_duplicates(child, parent1)

        return child

    
    def mutation(self, child):
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(len(child)), 2)
            child[i], child[j] = child[j], child[i]
        return child

    def genetic_algorithm(self, cities, distances):
        self.initiate_population(cities)
        if len(self.population) < self.population_size:
            raise ValueError(f"Population trop petite après initialisation: {len(self.population)}")
        
        cached_fitnesses = {}  # Cache pour stocker les fitness des chemins déjà calculés
        fitnesses = [self.fitness(way, distances, cached_fitnesses) for way in self.population]

        mutation_interval = 50  # Nombre de générations avant de muter 
        for generation in range(self.generations):
            new_population = []
            fitnesses = [self.fitness(way, distances, cached_fitnesses) for way in self.population]
        
            if len(fitnesses) < self.population_size:
                raise ValueError(f"Le nombre de fitnesses ({len(fitnesses)}) est inférieur à la taille de la population ({self.population_size})") 
            
            while len(new_population) < self.population_size:
                parent1, parent2 = self.selection_type_selection(self.population, fitnesses)

                child1 = self.crossover(parent1, parent2)
                child2 = self.crossover(parent2, parent1)

                # Appliquer la mutation toutes les "mutation_interval" générations
                if mutation_interval > 0 and generation % mutation_interval == 0:
                    child1 = self.mutation(child1)
                    child2 = self.mutation(child2)

                new_population.append(child1)
                if len(new_population) < self.population_size:
                    new_population.append(child2)

            if len(new_population) != self.population_size:
                raise ValueError(f"Nouvelle population trop petite après la génération {generation}: {len(new_population)}")

            # On remplace l'ancienne population par la nouvelle
            self.population = new_population

            # On retourne le meilleur chemin
            best_way = max(self.population, key=lambda x:  self.fitness(x, distances, cached_fitnesses))

        return best_way
    def remove_duplicates(self,child, parent):
        missing = [city for city in parent if city not in child]
        seen = set()
        duplicates = [i for i, city in enumerate(child) if city in seen or seen.add(city)]

        for i in duplicates:
            child[i] = missing.pop(0)  

        return child


   