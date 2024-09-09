import pandas as pd
import matplotlib.pyplot as plt
import mpl_toolkits
from mpl_toolkits.basemap import Basemap

df = pd.read_csv('./Docs/villes_france_lat_long.csv', sep=',')

print(df.head())

# affichage 2D des points

plt.scatter(df['Latitude'], df['Longitude'])
# plt.show()

# utilisation d'un globe terrestre pour afficher les points sur une carte en 3D zoomée sur la France

m = Basemap(projection='ortho', lat_0=45, lon_0=0)

m.drawcoastlines()
m.drawcountries()
m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='coral', lake_color='aqua')

x, y = m(df['Longitude'].values, df['Latitude'].values)

m.scatter(x, y, color='red')

plt.show()