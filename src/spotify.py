
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

elt = {
    'track': "The Less I Know The Better",
    'artist':  "Tame Impala"
}

def get_spotify_uri(elt):
    query = f"track:{elt['track']} artist:{elt['artist']}"

    results = spotify.search(q=query, type='track', limit=1)
    items = results['tracks']['items']
    if len(items) > 0:
        track = items[0]
        return(
            {
                'spotify_uri': track['uri'],
                'release_date': track['album']['release_date'],
                'popularity': track['popularity'],
                'duration_ms': track['duration_ms'],
                'explicit': track['explicit']
            }
        )
    

print(get_spotify_uri(elt))