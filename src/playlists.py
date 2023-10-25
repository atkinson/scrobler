import os
import base64
import http.client as http_client
import json

from urllib.parse import urlencode
import webbrowser

import requests
from google.cloud import firestore

from scrobler.config import db, firebase_collection

http_client.HTTPConnection.debuglevel = 1

songs = db.collection(firebase_collection).get()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
PLAYLIST_ID = "3y0nCSkB0ceFKsKBjEDyk1"
SPOTIFY_CALLBACK_URL = "http://localhost:8080/callback"

SPOTIFY_AUTHORIZATION_CODE = "Generated using auth.py"

ENCODED_CREDENTIALS = base64.b64encode(
    f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode("ascii")
).decode("ascii")


# res = requests.post(
#     url="https://accounts.spotify.com/api/token",
#     headers={
#         "Authorization": f"Basic {ENCODED_CREDENTIALS}",
#         "Content-Type": "application/x-www-form-urlencoded",
#     },
#     data={
#         "grant_type": "authorization_code",
#         "code": SPOTIFY_AUTHORIZATION_CODE,
#         "redirect_uri": SPOTIFY_CALLBACK_URL,
#     },
# )

# print(res.json())

# ACCESS_TOKEN = res.json()["access_token"]
ACCESS_TOKEN = "generated from the above, the access token can be used to make requests to the Spotify API"


def split_into_chunks(lst, n):
    """Split a list into chunks of length n."""
    # Initialize an empty list to store the chunks
    chunks = []

    # Loop through the list and slice it into chunks of length n
    for i in range(0, len(lst), n):
        chunks.append(lst[i : i + n])

    return chunks


# print("****** test ****")
# res = requests.get(
#     url=f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}",
#     headers={
#         "Authorization": f"Bearer {ACCESS_TOKEN}",
#         "Content-type": "application/json",
#         "Accept": "text/plain",
#     },
# )

# print(res.text)


# iterate over songs
ids = []
for song in songs:
    if song.to_dict().get("spotify_uri"):
        ids.append(song.to_dict()["spotify_uri"])

for chunk in split_into_chunks(ids, 100):
    data = {"uris": chunk}
    res = requests.post(
        url=f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        json=data,
    )
    if res.status_code == 400:
        print(res.text)
        raise Exception("400")
