import os
import base64
import http.client as http_client
import json

from urllib.parse import urlencode
import webbrowser

import requests

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_CALLBACK_URL = "http://localhost:8080/callback"


auth_headers = {
    "client_id": SPOTIFY_CLIENT_ID,
    "response_type": "code",
    "redirect_uri": SPOTIFY_CALLBACK_URL,
    "scope": "user-library-read, playlist-modify-public playlist-modify-private",
}

webbrowser.open(
    "https://accounts.spotify.com/authorize?"
    + urlencode(auth_headers)
)
