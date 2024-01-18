import os
import base64
import http.client as http_client
import json

from urllib.parse import urlencode
import webbrowser

from flask import Flask, request

import requests

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_CALLBACK_URL = "http://localhost:8080/callback"


app = Flask(__name__)


def get_authorization_code():
    auth_headers = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": SPOTIFY_CALLBACK_URL,
        "scope": "user-library-read, playlist-modify-public playlist-modify-private",
    }
    webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))


@app.route("/callback")
def myapp():
    SPOTIFY_AUTHORIZATION_CODE = request.args.get("code")
    ENCODED_CREDENTIALS = base64.b64encode(
        f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode("ascii")
    ).decode("ascii")

    res = requests.post(
        url="https://accounts.spotify.com/api/token",
        headers={
            "Authorization": f"Basic {ENCODED_CREDENTIALS}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "authorization_code",
            "code": SPOTIFY_AUTHORIZATION_CODE,
            "redirect_uri": SPOTIFY_CALLBACK_URL,
        },
    )

    print(res.json())

    os.environ["SPOTIFY_ACCESS_TOKEN"] = res.json()["access_token"]
    return res.json()["access_token"]


get_authorization_code()
