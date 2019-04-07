#!/usr/bin/env python

from flask import request
import requests


URL = "https://oauth2.googleapis.com/tokeninfo"


def get_data_from_token(id_token):
    # print(id_token)
    NEW_URL = URL + "?id_token=" + id_token
    response = requests.get(url=NEW_URL)
    id_info = response.json()

    #profile_name = id_info["name"]
    #email_id = id_info["email"]
    #picture = id_info["picture"]

    if(id_info["name"] and id_info["email"]):
        return id_info
    return None
