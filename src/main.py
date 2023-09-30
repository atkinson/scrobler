import re
import hashlib
import requests
from bs4 import BeautifulSoup
from google.cloud import firestore

# gcloud iam service-accounts create scrobbler
# gcloud projects add-iam-policy-binding air-paradise --member="serviceAccount:scrobbler@air-paradise.iam.gserviceaccount.com" --role=roles/firebase.admin
# gcloud iam service-accounts add-iam-policy-binding scrobbler@air-paradise.iam.gserviceaccount.com --member="user:rich@airteam.com.au" --role=roles/iam.serviceAccountUser
URL = "http://www8.radioparadise.com/rp3-mx.php?n=Playlist"

gcp_project = "air-paradise"
db = firestore.Client(project=gcp_project)


def parse(track):
    """Remove the timestamp
    returns a tuple (artist, title)
    """
    return re.sub(
        "^([0-1]?[0-9]|2[0-3]):[0-5][0-9] [ap]m", "", track.get_text()
    ).split(" - ")


def store(key, artist, title, dummy=False):
    if dummy:
        print("artist: {}, title: {}".format(artist, title))
        return
    doc_ref = db.collection("radio_paradise").document(key)
    doc_ref.set({"artist": artist, "title": title}, merge=True)


def mainHTTP(request):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    for track in soup.select('div[class*="p-row"]'):
        artist, title = parse(track)
        key = hashlib.md5(bytes(artist + title, "utf-8")).hexdigest()
        store(key, artist, title)

    return "ok"

mainHTTP("test")