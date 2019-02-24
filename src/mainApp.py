#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests
import json
import os
import requests
import traceback

import quizSection
import storeInDemoDB
import tokenSection


app = Flask(__name__)


QUESTION_NUMBER = 0
DIFFICULTY_LEVEL = 1
CORRECT_ANS = ""
CURRENT_QUESTION_ITEMS = []

ERROR_PAGE_TEMPLATE_FILE = "error_page.html"
INDEX_PAGE_TEMPLATE_FILE = "index_page.html"
DASHBOARD_PAGE_TEMPLATE_FILE = "dashboard.html"
QUIZ_RULE_PAGE_TEMPLATE_FILE = "quiz_rules_page.html"
MCQ_QUIZ_PAGE_TEMPLATE_FILE = "mcq_quiz_page.html"
SUBJECTIVE_QUIZ_PAGE_TEMPLATE_FILE = "subjective_quiz_page.html"
RESULT_PAGE_TEMPLATE_FILE = 'result_page.html'


@app.route("/")
def index():
    global INDEX_PAGE_TEMPLATE_FILE
    global QUESTION_NUMBER
    QUESTION_NUMBER = 0

    return render_template(INDEX_PAGE_TEMPLATE_FILE)


@app.route("/get_started", methods=["GET", "POST"])
def get_started():
    global DASHBOARD_PAGE_TEMPLATE_FILE, ERROR_PAGE_TEMPLATE_FILE
    global QUESTION_NUMBER
    QUESTION_NUMBER = 0

    try:
        if(request.method == "POST"):
            id_token = request.form.get("idToken")

            id_info = tokenSection.get_data_from_token(id_token)
            if(bool(id_info)):
                return render_template(
                    DASHBOARD_PAGE_TEMPLATE_FILE,
                    id_token=id_token,
                    id_info=id_info)

        return render_template(ERROR_PAGE_TEMPLATE_FILE)

    except BaseException:
        traceback.print_exc()


@app.route("/quiz_rules", methods=["GET", "POST"])
def quiz_rules():
    global QUIZ_RULE_PAGE_TEMPLATE_FILE, ERROR_PAGE_TEMPLATE_FILE
    global QUESTION_NUMBER
    QUESTION_NUMBER = 0

    try:
        if(request.method == "POST"):
            id_token = request.form.get("idToken")
            topic = request.form.get("topic")

            id_info = tokenSection.get_data_from_token(id_token)
            if(bool(id_info)):
                return render_template(
                    QUIZ_RULE_PAGE_TEMPLATE_FILE,
                    id_token=id_token,
                    topic=topic)

        return render_template(ERROR_PAGE_TEMPLATE_FILE)

    except BaseException:
        traceback.print_exc()


def predict_difficulty(CORRECT_ANS, previous_ans_ticked, DIFFICULTY_LEVEL):
    if CORRECT_ANS == previous_ans_ticked and DIFFICULTY_LEVEL <= 2:
        DIFFICULTY_LEVEL += 1

    elif DIFFICULTY_LEVEL >= 2:
        DIFFICULTY_LEVEL -= 1

    return DIFFICULTY_LEVEL


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    global MCQ_QUIZ_PAGE_TEMPLATE_FILE, SUBJECTIVE_QUIZ_PAGE_TEMPLATE_FILE, ERROR_PAGE_TEMPLATE_FILE
    global DIFFICULTY_LEVEL, CURRENT_QUESTION_ITEMS, CORRECT_ANS
    global QUESTION_NUMBER

    template_file = ""

    try:
        if(request.method == "POST"):
            id_token = request.form.get("idToken")
            topic = request.form.get("topic")
            previous_ans_ticked = request.form.get("answerTicked")
            previous_time_taken = request.form.get("timeTaken")

            id_info = tokenSection.get_data_from_token(id_token)
            if(bool(id_info)):
                if previous_time_taken is not None:
                    CURRENT_QUESTION_ITEMS.append(previous_time_taken)
                    if QUESTION_NUMBER <= 10:
                        CURRENT_QUESTION_ITEMS.append(previous_ans_ticked)
                    storeInDemoDB.store_in_DB(CURRENT_QUESTION_ITEMS)

                QUESTION_NUMBER += 1

                if(topic == "Miscellaneous"):
                    question_item = quizSection.demo_questions(
                        topic, QUESTION_NUMBER)

                elif topic in ["Sports", "GK", "Technology"]:
                    DIFFICULTY_LEVEL = predict_difficulty(
                        CORRECT_ANS, previous_ans_ticked, DIFFICULTY_LEVEL)
                    question_item = quizSection.main_questions(
                        topic, QUESTION_NUMBER, DIFFICULTY_LEVEL)

                if bool(question_item) and QUESTION_NUMBER <= 10:
                    CURRENT_QUESTION_ITEMS = [
                        QUESTION_NUMBER,
                        question_item["question_type"],
                        question_item["difficulty_level"],
                        question_item["question"],
                        question_item["correct_answer"],
                        question_item["description"],
                        question_item["time_limit"]
                    ]

                    if QUESTION_NUMBER < 10:
                        CORRECT_ANS = question_item["correct_answer"]
                        template_file = MCQ_QUIZ_PAGE_TEMPLATE_FILE

                    elif QUESTION_NUMBER == 10:
                        template_file = SUBJECTIVE_QUIZ_PAGE_TEMPLATE_FILE

                    return render_template(
                        template_file,
                        id_token=id_token,
                        id_info=id_info,
                        question_no=QUESTION_NUMBER,
                        question_item=question_item
                    )

        if QUESTION_NUMBER > 10:
            # return redirect(url_for('result_page', id_info=id_info))
            return redirect(url_for('result_page'))

        return render_template(ERROR_PAGE_TEMPLATE_FILE)

    except BaseException:
        traceback.print_exc()


@app.route("/result", methods=["GET", "POST"])
def result_page():
    #id_token = request.form.get['id_token']
    # print(request.form)
    return render_template(RESULT_PAGE_TEMPLATE_FILE)


if __name__ == "__main__":
    app.run()
