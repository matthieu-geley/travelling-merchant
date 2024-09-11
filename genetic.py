import random
from math import radians, sin, cos, sqrt, atan2
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
    
    def calculer_distance(self, way, df):
        distance = 0
        #coordonnées des villes directement depuis le DataFrame
        for i in range(len(way) - 1):
            city1 = way[i]
            city2 = way[i + 1]
            lat1, lon1 = df.loc[df['Ville'] == city1, ['Latitude', 'Longitude']].values[0]
            lat2, lon2 = df.loc[df['Ville'] == city2, ['Latitude', 'Longitude']].values[0]
            distance += self.haversine(lon1, lat1, lon2, lat2)
        return distance

    def genetic_algorithm(self, cities):
        
        self.initiate_population(cities)
        if len(self.population) < self.population_size:
            raise ValueError(f"Population trop petite après initialisation: {len(self.population)}")

        for generation in range(self.generations):
            new_population = []

            fitnesses = [self.fitness(way, cities) for way in self.population]
            if len(fitnesses) < self.population_size:
                raise ValueError(f"Le nombre de fitnesses ({len(fitnesses)}) est inférieur à la taille de la population ({self.population_size})") 
            
            while len(new_population) < self.population_size:
                parent1, parent2 = self.selection_type_selection(self.population, fitnesses)

                child1 = self.crossover(parent1, parent2)

                child1 = self.mutation(child1)

                new_population.append(child1)
            if len(new_population) != self.population_size:
                raise ValueError(f"Nouvelle population trop petite après la génération {generation}: {len(new_population)}")

            # On remplace l'ancienne population par la nouvelle
            self.population = new_population

            # On retourne le meilleur chemin
            best_way = max(self.population, key=lambda x: self.fitness(x, cities))
            return best_way
    def fitness(self, way, cities):
        return 1 / self.calculer_distance(way, cities)
    
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
        child[start:end] = parent1[start:end]
        remaining = [x for x in parent2 if x not in child]
        child[:start] = [x for x in remaining[:start] if x != -1]
        child[end:] = [x for x in remaining[start:] if x != -1]
        return child
    
    def pmx_crossover(self, parent1, parent2):
        child = [-1] * len(parent1)
        start, end = sorted(random.sample(range(len(parent1)), 2))
        child[start:end] = parent1[start:end]
        for i in range(start, end):
            if parent2[i] not in child:
                j = i
                while parent1[j] in child:
                    j = parent2.index(parent1[j])
                child[j] = parent2[i]
        for i in range(len(child)):
            if child[i] == -1:
                child[i] = parent2[i]
        return child
    
    def mutation(self, child):
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(len(child)), 2)
            child[i], child[j] = child[j], child[i]
        return child
    #representation graphique   
