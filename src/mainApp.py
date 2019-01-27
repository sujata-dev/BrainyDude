from flask import Flask, render_template, request, redirect, url_for, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests
import json
import os
import requests
import traceback

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('mainpage.html')


@app.route('/get_started', methods = ['GET', 'POST'])
def get_started():
    URL = "https://oauth2.googleapis.com/tokeninfo"
    try:
        if(request.method == 'POST'):
            id_token = request.form.get('idToken')

            profile_name = ""
            email_id = ""
            picture=""
            if(id_token):
                URL = URL + "?id_token=" + id_token
                response = requests.get(url = URL)
                data = response.json()

                if(data['name'] and data['email']):
                    profile_name = data['name']
                    email_id = data['email']
                    picture = data['picture']

        return render_template('dashboard.html',
            profile_name = profile_name, email_id = email_id, picture = picture)

    except:
        traceback.print_exc()




if __name__ == '__main__':
    app.run()
