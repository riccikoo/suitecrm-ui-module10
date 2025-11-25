import requests
from flask import request, redirect, flash

TOKEN_URL = "http://localhost/module10/public/Api/access_token"
CLIENT_ID = "28a99247-3767-43ea-f308-692421e042c6"
CLIENT_SECRET = "mod10-client"


def login_user(username, password):
    payload = {
        "grant_type": "password",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "username": username,
        "password": password
    }

    response = requests.post(TOKEN_URL, data=payload)

    if response.status_code != 200:
        return None, response.text

    return response.json(), None