# import pandas as pd
# import matplotlib.pyplot as plt
# import mpl_toolkits
# from mpl_toolkits.basemap import Basemap

# df = pd.read_csv('./Docs/villes_france_lat_long.csv', sep=',')

# print(df.head())

# # affichage 2D des points

# plt.scatter(df['Latitude'], df['Longitude'])
# # plt.show()

# # utilisation d'un globe terrestre pour afficher les points sur une carte en 3D zoomée sur la France

# m = Basemap(projection='ortho', lat_0=45, lon_0=0)

# m.drawcoastlines()
# m.drawcountries()
# m.drawmapboundary(fill_color='aqua')
# m.fillcontinents(color='coral', lake_color='aqua')

# x, y = m(df['Longitude'].values, df['Latitude'].values)

# m.scatter(x, y, color='red')

# plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from math import radians, sin, cos, sqrt, atan2

# Fonction pour calculer la distance de Haversine entre deux points (en km)
def haversine(lon1, lat1, lon2, lat2):
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

# On charge les données
df = pd.read_csv('./Docs/villes_france_lat_long.csv', sep=',').head(20)
print(df.head())

# On crée la carte avec projection ortho centrée sur la France
fig = plt.figure(figsize=(10, 5))
ax = plt.axes(projection=ccrs.Orthographic(central_longitude=0, central_latitude=45))

# On ajoute des traits côtiers et frontières
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)

# On ajoute des points des villes françaises
plt.scatter(df['Longitude'], df['Latitude'], color='red', transform=ccrs.PlateCarree())

# On récupère les coordonnées des villes
lats = df['Latitude'].values
lons = df['Longitude'].values
villes = df['Ville'].values

# On ajoute des routes entre les villes et on calcule des distances
for i in range(len(lats)):
    for j in range(i + 1, len(lats)):
        lon1, lat1 = lons[i], lats[i]
        lon2, lat2 = lons[j], lats[j]
        
        # On calcule de la distance entre les deux villes
        distance = haversine(lon1, lat1, lon2, lat2)
        print(f"Distance entre {villes[i]} et {villes[j]}: {distance:.2f} km")
        
        # On trace la ligne entre les villes
        plt.plot([lon1, lon2], [lat1, lat2], color='blue', linewidth=0.5, transform=ccrs.PlateCarree())
        
        # Position centrale pour afficher la distance
        lon_mid = (lon1 + lon2) / 2
        lat_mid = (lat1 + lat2) / 2
        
        # On affiche la distance sur la carte
        plt.text(lon_mid, lat_mid, f'{distance:.0f} km', color='black', fontsize=6, ha='center', transform=ccrs.PlateCarree())

# On affiche la carte
plt.show()

