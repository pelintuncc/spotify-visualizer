import sys
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

# Add the project directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# Spotify API connection
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=config.CLIENT_ID,
    client_secret=config.CLIENT_SECRET,
    redirect_uri="http://localhost:8080",
    scope="playlist-read-private"
))

# fetch playlist tracks
def fetch_playlist_tracks(playlist_id, market="US"):
    """
    fetches a list of playlists from Spotify API

    args:
        playlist_id (str): Spotify playlist ID
        market (str): ISO 3166-1 alpha-2 country code
  
    Returns:
        list of playlists
    """
    try:
        results = sp.playlist_tracks(playlist_id, market=market)
        tracks = []
        for item in results.get('items', []):
            track = item.get('track')
            if not track:
                print(f"Skipping item with missing track: {item}")
                continue

            artists = track.get('artists')
            album = track.get('album')

            if not artists or not album:
                print(f"Skipping track with missing artists or album: {track}")
                continue

            tracks.append({
                'Name': track.get('name', 'Unknown'),
                'Artist': artists[0].get('name', 'Unknown Artist') if artists else 'Unknown Artist',
                'Album': album.get('name', 'Unknown Album') if album else 'Unknown Album',
                'Popularity': track.get('popularity', 0),
                'Duration_ms': track.get('duration_ms', 0)
            })
        return tracks
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

# save tracks to csv
def save_tracks_to_csv(tracks, file_path):
    """
    Şarkı detaylarını bir CSV dosyasına kaydeder.

    Args:
        tracks (list): Şarkı detaylarının listesi
        file_path (str): Kaydedilecek dosyanın yolu
    """
    try:
        if not tracks:
            print("No tracks to save.")
            return

       
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        df = pd.DataFrame(tracks)
        df.to_csv(file_path, index=False)
        print(f"Veriler '{file_path}' dosyasına kaydedildi.")
    except Exception as e:
        print(f"Error saving tracks to CSV: {e}")

# main function
if __name__ == "__main__":
    # Playlist ID'si
    playlist_id = "1Hnqv2Z8rJZfHhCdd2Gk1C"  #my playlist
    market = "TR"

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(project_root, "data/playlist_tracks.csv")

    print(f"Saving file to: {file_path}") 
    tracks = fetch_playlist_tracks(playlist_id, market=market)
    if tracks:
        save_tracks_to_csv(tracks, file_path)



