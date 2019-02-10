from flask import Flask, render_template, request, redirect, url_for, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests
import json
import os
import csv
import requests
import traceback

app = Flask(__name__)
URL = "https://oauth2.googleapis.com/tokeninfo"
DEMO_QUESTIONS_FILE = "demoQuizMCQs.csv"
QUESTION_NUMBER = 1


@app.route("/")
def index():
    QUESTION_NUMBER = 1
    return render_template("mainpage.html")


@app.route("/get_started", methods=["GET", "POST"])
def get_started():
    QUESTION_NUMBER = 1
    try:
        if(request.method == "POST"):
            id_token = request.form.get("idToken")

            profile_name = ""
            email_id = ""
            picture = ""
            if(id_token):
                NEW_URL = URL + "?id_token=" + id_token
                response = requests.get(url=NEW_URL)
                data = response.json()

                if(data["name"] and data["email"]):
                    profile_name = data["name"]
                    email_id = data["email"]
                    picture = data["picture"]

        return render_template(
            "dashboard.html",
            id_token=id_token,
            profile_name=profile_name,
            email_id=email_id,
            picture=picture)

    except BaseException:
        traceback.print_exc()


@app.route("/quiz_rules", methods=["GET", "POST"])
def quiz_rules():
    QUESTION_NUMBER = 1
    try:
        if(request.method == "POST"):
            id_token = request.form.get("idToken")

            if(id_token):
                NEW_URL = URL + "?id_token=" + id_token
                response = requests.get(url=NEW_URL)

        return render_template(
            "quiz_rules_page.html",
            id_token=id_token
        )

    except BaseException:
        traceback.print_exc()


def demo_questions(QUESTION_NUMBER):
    question_item = {}
    with open(DEMO_QUESTIONS_FILE) as file:
        reader = csv.DictReader(file)
        line_number_csv = QUESTION_NUMBER
        while(line_number_csv > 1):
            row = next(reader)
            line_number_csv = line_number_csv - 1

        for line in reader:
            if line["Difficulty Level"] in ["1", "2", "3"]:
                if line["Difficulty Level"] == "1":
                    question_item["Difficulty Level"] = "Easy"
                elif line["Difficulty Level"] == "2":
                    question_item["Difficulty Level"] = "Medium"
                elif line["Difficulty Level"] == "3":
                    question_item["Difficulty Level"] = "Hard"

                question_item["Question"] = line["Question"]
                question_item["Option A"] = line["Option A"]
                question_item["Option B"] = line["Option B"]
                question_item["Option C"] = line["Option C"]
                question_item["Option D"] = line["Option D"]
                question_item["Correct Answer"] = question_item["Option " +
                                                                line["Correct Answer"]]
                question_item["Description"] = line["Description"]
                break

        return question_item


@app.route("/demo_quiz", methods=["GET", "POST"])
def demo_quiz():
    global QUESTION_NUMBER
    question_type = "MCQ"

    try:
        if(request.method == "POST"):
            id_token = request.form.get("idToken")

            if(id_token):
                NEW_URL = URL + "?id_token=" + id_token
                response = requests.get(url=NEW_URL)
                data = response.json()

                if(data["name"] and data["email"]):
                    profile_name = data["name"]
                    email_id = data["email"]
                    picture = data["picture"]

                if QUESTION_NUMBER > 9:
                    question_type = "Subjective"

                question_item = demo_questions(QUESTION_NUMBER)
                QUESTION_NUMBER = QUESTION_NUMBER + 1

        return render_template(
            "mcq_quiz_page.html",
            id_token=id_token,
            profile_name=profile_name,
            email_id=email_id,
            picture=picture,
            question_no=QUESTION_NUMBER - 1,
            question_type=question_type,
            difficulty_level=question_item["Difficulty Level"],
            question=question_item["Question"],
            option_a=question_item["Option A"],
            option_b=question_item["Option B"],
            option_c=question_item["Option C"],
            option_d=question_item["Option D"]
        )

    except BaseException:
        traceback.print_exc()


if __name__ == "__main__":
    app.run()
