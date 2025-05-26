import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# load the .env file variables
load_dotenv()

# Spotify API credentials
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

lz_uri = 'spotify:artist:2o5jDhtHVPhrJdv3cEQ99Z'

top_tracks = sp.artist_top_tracks(lz_uri)

tracks_data = []
for track in top_tracks['tracks']:
    tracks_data.append({
        'Nombre': track['name'],
        'Popularidad': track['popularity'],
        'Duración (ms)': track['duration_ms'],
    })

df = pd.DataFrame(tracks_data)

df_sorted = df.sort_values(by='Popularidad', ascending=True)
top_3_menos_populares = df_sorted.head(3)

print("Top 3 canciones menos populares:")
print(top_3_menos_populares[['Nombre', 'Popularidad', 'Duración (ms)']])

# Convertir la duración de milisegundos a minutos para mejor interpretación
df['Duración (min)'] = df['Duración (ms)'] / 60000

# Crear el scatterplot
plt.figure(figsize=(10, 6))
plt.scatter(df['Duración (min)'], df['Popularidad'], alpha=0.6, edgecolors='w', s=100)

# Añadir títulos y etiquetas
plt.title('Relación entre Duración y Popularidad de las Canciones', fontsize=14)
plt.xlabel('Duración (minutos)', fontsize=12)
plt.ylabel('Popularidad (0-100)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Añadir etiquetas con los nombres de las canciones
for i, row in df.iterrows():
    plt.text(row['Duración (min)']+0.02, row['Popularidad']+1, row['Nombre'], 
             fontsize=8, alpha=0.7)

# Mostrar el gráfico
plt.tight_layout()
plt.show()
