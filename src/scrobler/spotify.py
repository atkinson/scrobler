import json
from datetime import date
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

conn = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def get_spotify_meta(elt):
    query = f"track:{elt['title']} artist:{elt['artist']}"
    results = conn.search(q=query, type="track", limit=1)
    items = results["tracks"]["items"]
    if len(items) > 0:
        track = items[0]
        return {
            "spotify_uri": track["uri"],
            "release_date": track["album"]["release_date"],
            "popularity": track["popularity"],
            "duration_ms": track["duration_ms"],
            "explicit": track["explicit"],
            "last_updated": date.today().strftime("%Y-%m-%d"),
        }


def add_to_playlist(playlist_id, spotify_uri_list):
    conn.playlist_add_items(playlist_id, spotify_uri_list)
