import os
import http.client as http_client
import json

import requests
from scrobler.config import db, firebase_collection, SPOTIFY_PLAYLIST_2024

http_client.HTTPConnection.debuglevel = 1

songs = db.collection(firebase_collection).get()

PLAYLIST_ID = SPOTIFY_PLAYLIST_2024
ACCESS_TOKEN = os.getenv("SPOTIFY_ACCESS_TOKEN")  # get from auth.py
ACCESS_TOKEN = "BQDdu4jHt-4Mc25QejXao2c58OvBGTNofFYKgM4gf2MfbfobF9uxyTocM1Z6geBFXlvF5FNbllY_m-0NfaxKCF_jgCcDb3qQkirAGIyB5tp9MGQiXEh38Vj-6krxMBVgkvs0kAlw3WosCHppbnByuei65HbBjUScbwTko--eftcJK2W0ES-J2lcZBamR1msF19IcFu3sFwZ1WFRLph43Fba9MvpIvr4v96hPgYu96A02fMqefMJm"


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


def empty_playlist(playlist_id):
    res = requests.put(
        url=f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        json={"uris": []},
    )


empty_playlist(PLAYLIST_ID)
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
