import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import seaborn as sns

# cargar variables del archivo .env
load_dotenv()

# verificar credenciales
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

# inicializar cliente de Spotify
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
spotify = spotipy.Spotify(auth_manager=auth_manager)

# URI correcto sin parámetros adicionales
lz_uri = 'spotify:artist:5XJDexmWFLWOkjOEjOVX3e'

# obtener las top tracks del artista
results = spotify.artist_top_tracks(lz_uri)

# crear lista para guardar datos
tracks_data = []

# listar las primeras 10 canciones
for track in results['tracks'][:10]:
    tracks_data.append({
        'nombre': track['name'],
        'artista': track['album']['artists'][0]['name'],
        'popularidad': track['popularity'],
        'duracion_ms': track['duration_ms'],
        'audio_url': track['preview_url'] or 'No disponible',
        'cover_art': track['album']['images'][0]['url']
    })
# Convertir la lista en DataFrame
df = pd.DataFrame(tracks_data)
df['duracion_min'] = df['duracion_ms'] / 60000  # de ms a minutos

# Ordenar por popularidad 
df_ordenado = df.sort_values(by='popularidad', ascending=False)

# Mostrar las 3 canciones con mayor popularidad
top3_mas_populares = df_ordenado.head(3)

print(top3_mas_populares)

#grafica
sns.scatterplot(data=df, x='duracion_min', y='popularidad')
plt.xlabel('Duración (minutos)')
plt.ylabel('Popularidad')
plt.title('Relación entre duración y popularidad de las canciones')
plt.show()