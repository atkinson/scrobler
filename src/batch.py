from google.cloud import firestore

from scrobler.config import db, firebase_collection
from scrobler.spotify import get_spotify_meta

songs = db.collection(firebase_collection).get()

# iterate over songs

for song in songs:
    print(song.to_dict())
    meta = get_spotify_meta(song.to_dict())
    db.collection(firebase_collection).document(song.id).set(meta)
