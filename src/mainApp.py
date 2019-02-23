from flask import Flask, render_template, request, redirect, url_for, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests
import json
import os
import requests
import traceback

import demoSection
import sportsSection
import storeInDemoDB


app = Flask(__name__)
URL = "https://oauth2.googleapis.com/tokeninfo"

QUESTION_NUMBER = 0
DIFFICULTY_LEVEL = 1
CORRECT_ANS = ""
CURRENT_ITEMS = []


@app.route("/")
def index():
    QUESTION_NUMBER = 0
    return render_template("mainpage.html")


@app.route("/get_started", methods=["GET", "POST"])
def get_started():
    global QUESTION_NUMBER
    QUESTION_NUMBER = 0
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
    global QUESTION_NUMBER
    QUESTION_NUMBER = 0
    try:
        if(request.method == "POST"):
            id_token = request.form.get("idToken")

            topic = request.form.get("topic")

            if(id_token):
                NEW_URL = URL + "?id_token=" + id_token
                response = requests.get(url=NEW_URL)

        return render_template(
            "quiz_rules_page.html",
            id_token=id_token,
            topic=topic
        )

    except BaseException:
        traceback.print_exc()


@app.route("/demo_quiz", methods=["GET", "POST"])
def demo_quiz():
    global QUESTION_NUMBER
    global CURRENT_ITEMS
    question_type = "MCQ"

    try:
        if(request.method == "POST"):
            id_token = request.form.get("idToken")
            topic = request.form.get("topic")

            previous_ans_ticked = request.form.get("answerTicked")
            previous_time_taken = request.form.get("timeTaken")

            if(id_token):
                NEW_URL = URL + "?id_token=" + id_token
                response = requests.get(url=NEW_URL)
                data = response.json()

                profile_name = ""
                email_id = ""
                picture = ""

                if(data["name"] and data["email"]):
                    profile_name = data["name"]
                    email_id = data["email"]
                    picture = data["picture"]

                QUESTION_NUMBER = QUESTION_NUMBER + 1

                if previous_time_taken is not None:
                    CURRENT_ITEMS.append(previous_time_taken)
                    if QUESTION_NUMBER <= 11:
                        CURRENT_ITEMS.append(previous_ans_ticked)
                    storeInDemoDB.store_in_DB(CURRENT_ITEMS)

                question_item = demoSection.demo_questions(QUESTION_NUMBER)

                if bool(question_item):
                    if QUESTION_NUMBER == 10:
                        question_type = "Subjective"
                        time_limit = 20
                        difficulty_level = "-"
                        description = "-"

                        CURRENT_ITEMS = [
                            QUESTION_NUMBER,
                            question_type,
                            difficulty_level,
                            question_item["Question"],
                            question_item["Correct Answer"],
                            description]

                        return render_template(
                            "subjective_quiz_page.html",
                            id_token=id_token,
                            profile_name=profile_name,
                            email_id=email_id,
                            picture=picture,
                            topic=topic,
                            question_no=QUESTION_NUMBER,
                            question_type=question_type,
                            difficulty_level=difficulty_level,
                            question=question_item["Question"],
                            time_limit=time_limit
                        )

                    CURRENT_ITEMS = [
                        QUESTION_NUMBER,
                        question_type,
                        question_item["Difficulty Level"],
                        question_item["Question"],
                        question_item["Correct Answer"],
                        question_item["Description"]]

                    return render_template(
                        "mcq_quiz_page.html",
                        id_token=id_token,
                        profile_name=profile_name,
                        email_id=email_id,
                        picture=picture,
                        topic=topic,
                        question_no=QUESTION_NUMBER,
                        question_type=question_type,
                        difficulty_level=question_item["Difficulty Level"],
                        question=question_item["Question"],
                        option_a=question_item["Option A"],
                        option_b=question_item["Option B"],
                        option_c=question_item["Option C"],
                        option_d=question_item["Option D"],
                        time_limit=question_item["Time Limit"]
                    )

        return render_template("result_page.html")

    except BaseException:
        traceback.print_exc()


@app.route("/main_quiz", methods=["GET", "POST"])
def main_quiz():
    global QUESTION_NUMBER
    global DIFFICULTY_LEVEL
    global CORRECT_ANS
    question_type = "MCQ"

    try:
        if(request.method == "POST"):
            id_token = request.form.get("idToken")
            topic = request.form.get("topic")

            ans_ticked = request.form.get("answerTicked")
            time_taken = request.form.get("timeTaken")

            if(id_token):
                NEW_URL = URL + "?id_token=" + id_token
                response = requests.get(url=NEW_URL)
                data = response.json()

                profile_name = ""
                email_id = ""
                picture = ""

                if(data["name"] and data["email"]):
                    profile_name = data["name"]
                    email_id = data["email"]
                    picture = data["picture"]

                QUESTION_NUMBER = QUESTION_NUMBER + 1

                if CORRECT_ANS == ans_ticked:
                    if DIFFICULTY_LEVEL <= 2:
                        DIFFICULTY_LEVEL += 1

                else:
                    if DIFFICULTY_LEVEL >= 2:
                        DIFFICULTY_LEVEL -= 1

                question_item = sportsSection.sports_questions(
                    topic, QUESTION_NUMBER, DIFFICULTY_LEVEL)
                CORRECT_ANS = question_item["Correct Answer"]

                if QUESTION_NUMBER == 10:
                    question_type = "Subjective"
                    time_limit = 20
                    difficulty_level = "-"

                    return render_template(
                        "subjective_quiz_page.html",
                        id_token=id_token,
                        profile_name=profile_name,
                        email_id=email_id,
                        picture=picture,
                        topic=topic,
                        question_no=QUESTION_NUMBER,
                        question_type=question_type,
                        difficulty_level=difficulty_level,
                        question=question_item["Question"],
                        time_limit=time_limit
                    )

        return render_template(
            "mcq_quiz_page.html",
            id_token=id_token,
            profile_name=profile_name,
            email_id=email_id,
            picture=picture,
            topic=topic,
            question_no=QUESTION_NUMBER,
            question_type=question_type,
            difficulty_level=question_item["Difficulty Level"],
            question=question_item["Question"],
            option_a=question_item["Option A"],
            option_b=question_item["Option B"],
            option_c=question_item["Option C"],
            option_d=question_item["Option D"],
            time_limit=question_item["Time Limit"]
        )

    except BaseException:
        traceback.print_exc()


@app.route("/result", methods=["GET", "POST"])
def result_page():
    print("hi")
    if(request.method == "POST"):
        print(request.form)

    return render_template("result_page.html")


if __name__ == "__main__":
    app.run()
