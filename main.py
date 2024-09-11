
import pandas as pd 
from genetic import AlgorithmeGenetiqueTSP
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from math import radians, sin, cos, sqrt, atan2
from christofides import christofides

"""
Fonction de Haversine pour calculer la distance de Haversine entre deux points en kilomètre.
1. On convertit les degrés en radians
2. On calcule la différence des coordonnées
3. On crée la formule d'Haversine
4. On retourne la distance en kilomètre
"""
def haversine(lon1, lat1, lon2, lat2):
    R = 6371.0  # Rayon de la Terre en km

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

"""
Fonction qui nous permet d'afficher la carte avec toutes les villes et les distances.
1. On crée la carte avec projection orthocentrée sur la France
2. On ajoute les points représentants les villes
3. On ajoute les routes et les distances
4. On affiche la carte
"""
def afficher_carte_villes(df):
    fig = plt.figure(figsize=(10, 5))
    ax = plt.axes(projection=ccrs.Orthographic(central_longitude=0, central_latitude=45))
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS)
    
    plt.scatter(df['Longitude'], df['Latitude'], color='red', transform=ccrs.PlateCarree())
    
    lats = df['Latitude'].values
    lons = df['Longitude'].values
    villes = df['Ville'].values
    
    for i in range(len(lats)):
        for j in range(i + 1, len(lats)):
            lon1, lat1 = lons[i], lats[i]
            lon2, lat2 = lons[j], lats[j]
            distance = haversine(lon1, lat1, lon2, lat2)
            print(f"Distance entre {villes[i]} et {villes[j]}: {distance:.2f} km")
            plt.plot([lon1, lon2], [lat1, lat2], color='blue', linewidth=0.5, transform=ccrs.PlateCarree())
            
            lon_mid = (lon1 + lon2) / 2
            lat_mid = (lat1 + lat2) / 2
            plt.text(lon_mid, lat_mid, f'{distance:.0f} km', color='black', fontsize=6, ha='center', transform=ccrs.PlateCarree())
    
    plt.title("Carte des villes françaises avec distances")
    plt.show()

"""
Fonction qui nous permet d'afficher la carte avec le chemin trouvé par l'algorithme de Christofides
1. On crée la carte avec projection orthocentrée sur la France
2. On ajoute les points représentants les villes
3. On ajoute les routes du chemin trouvé par l'algorithme de Christofides
4. On affiche la carte
"""
def afficher_carte_christofides(df, villes, chemin):
    fig = plt.figure(figsize=(10, 5))
    ax = plt.axes(projection=ccrs.Orthographic(central_longitude=0, central_latitude=45))
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS)
    
    plt.scatter(df['Longitude'], df['Latitude'], color='red', transform=ccrs.PlateCarree())
    
    total_distance = 0
    for i in range(len(chemin) - 1):
        ville1 = chemin[i]
        ville2 = chemin[i + 1]
        lon1, lat1 = villes[ville1]
        lon2, lat2 = villes[ville2]
        
        distance = haversine(lon1, lat1, lon2, lat2)
        total_distance += distance
        plt.plot([lon1, lon2], [lat1, lat2], color='blue', linewidth=0.5, transform=ccrs.PlateCarree())
        
        lon_mid = (lon1 + lon2) / 2
        lat_mid = (lat1 + lat2) / 2
        plt.text(lon_mid, lat_mid, f'{distance:.0f} km', color='black', fontsize=6, ha='center', transform=ccrs.PlateCarree())
    
    # Ajouter la ligne pour retourner au point de départ
    ville1 = chemin[-1]
    ville2 = chemin[0]
    lon1, lat1 = villes[ville1]
    lon2, lat2 = villes[ville2]
    distance = haversine(lon1, lat1, lon2, lat2)
    total_distance += distance
    plt.plot([lon1, lon2], [lat1, lat2], color='blue', linewidth=0.5, transform=ccrs.PlateCarree())
    lon_mid = (lon1 + lon2) / 2
    lat_mid = (lat1 + lat2) / 2
    plt.text(lon_mid, lat_mid, f'{distance:.0f} km', color='black', fontsize=6, ha='center', transform=ccrs.PlateCarree())

    plt.title(f"Chemin trouvé par l'algorithme de Christofides\nDistance totale: {total_distance:.2f} km")
    plt.show()

# On charge les données
df = pd.read_csv('./Docs/villes_france_lat_long.csv', sep=',').head(20)

# On affiche la première carte des villes et distances
afficher_carte_villes(df)

# On crée le dictionnaire des villes avec les coordonnées 
villes = {row['Ville']: (row['Longitude'], row['Latitude']) for _, row in df.iterrows()}

# On applique l'algorithme de Christofides
chemin = christofides(villes)

# On affiche la seconde carte avec le chemin optimisé
afficher_carte_christofides(df, villes, chemin)
df = pd.read_csv('Docs/villes_france_lat_long.csv', sep=',').head(20)
algorithme = AlgorithmeGenetiqueTSP(
    population_size=700,        
    selection_type='roulette_wheel', # Type de sélection ('roulette_wheel', 'tournament', etc.)
    reproduction_type='pmx',    # Type de croisement ('order' ou 'pmx')
    mutation_rate=0.02,         
    generations=500             
)
meilleur_chemin = algorithme.genetic_algorithm(df)
print("Meilleur chemin trouvé :", meilleur_chemin)
print("Distance totale :", algorithme.calculer_distance(meilleur_chemin, df))
