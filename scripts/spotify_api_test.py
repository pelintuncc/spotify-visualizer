import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

# Spotify API kimlik bilgilerini kullanarak bağlantıyı kur
credentials = SpotifyClientCredentials(
    client_id=config.CLIENT_ID,
    client_secret=config.CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=credentials)

# Test: Spotify'dan popüler şarkıları listele
try:
    results = sp.search(q='popular', limit=5)
    for idx, track in enumerate(results['tracks']['items']):
        print(f"{idx + 1}. {track['name']} - {track['artists'][0]['name']}")
except Exception as e:
    print(f"Bir hata oluştu: {e}")
