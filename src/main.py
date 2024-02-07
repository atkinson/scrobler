import re
import hashlib
import requests
from bs4 import BeautifulSoup
from google.cloud import firestore

from scrobler.config import db, firebase_collection

from scrobler.spotify import get_spotify_meta

# gcloud iam service-accounts create scrobbler
# gcloud projects add-iam-policy-binding air-paradise --member="serviceAccount:scrobbler@air-paradise.iam.gserviceaccount.com" --role=roles/firebase.admin
# gcloud iam service-accounts add-iam-policy-binding scrobbler@air-paradise.iam.gserviceaccount.com --member="user:rich@airteam.com.au" --role=roles/iam.serviceAccountUser
URL = "http://www8.radioparadise.com/rp3-mx.php?n=Playlist"


def parse(track):
    """Remove the timestamp
    returns a tuple (artist, title)
    """
    return re.sub(
        "^([0-1]?[0-9]|2[0-3]):[0-5][0-9] [ap]m",
        "",
        track.get_text(),
    ).split(" - ", 1)


def store(key, artist, title, dummy=False):
    if dummy:
        print("artist: {}, title: {}".format(artist, title))
        return
    elt = {
        "title": title,
        "artist": artist,
    }
    spotify_meta = get_spotify_meta(elt)

    doc_ref = db.collection(firebase_collection).document(key)
    (
        doc_ref.set({**elt, **spotify_meta}, merge=True)
        if spotify_meta
        else doc_ref.set(elt, merge=True)
    )


def mainHTTP(request):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    for track in soup.select('div[class*="p-row"]'):
        artist, title = parse(track)
        key = hashlib.md5(bytes(artist + title, "utf-8")).hexdigest()
        store(key, artist, title, dummy=False)

    return "ok"
