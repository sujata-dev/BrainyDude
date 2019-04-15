#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests
import json
import os
import requests
import traceback
import ast

import quizSection
import storeInDB
import tokenSection


app = Flask(__name__)

ERROR_PAGE_TEMPLATE_FILE = "error_page.html"
INDEX_PAGE_TEMPLATE_FILE = "index_page.html"
DASHBOARD_PAGE_TEMPLATE_FILE = "dashboard.html"
QUIZ_RULE_PAGE_TEMPLATE_FILE = "quiz_rules_page.html"
MCQ_QUIZ_PAGE_TEMPLATE_FILE = "mcq_quiz_page.html"
SUBJECTIVE_QUIZ_PAGE_TEMPLATE_FILE = "subjective_quiz_page.html"
RESULT_PAGE_TEMPLATE_FILE = 'result_page.html'
ALREADY_ATTEMPTED_DEMO_QUIZ_TEMPLATE_FILE = 'already_attempted_demo_quiz.html'
STATS_AVAILABLE_TEMPLATE_FILE = "stats_available.html"
STATS_NOT_AVAILABLE_TEMPLATE_FILE = "no_stats_available.html"
PRIVACY_POLICY_PAGE = "privacy_policy.html"


@app.route("/privacy_policy")
def privacy_policy():
    return render_template(PRIVACY_POLICY_PAGE)



@app.route("/")
def index():
    global INDEX_PAGE_TEMPLATE_FILE

    return render_template(INDEX_PAGE_TEMPLATE_FILE)


@app.route("/get_started", methods=["GET", "POST"])
def get_started():
    global DASHBOARD_PAGE_TEMPLATE_FILE, ERROR_PAGE_TEMPLATE_FILE

    try:
        if(request.method == "POST"):
            id_token = request.form.get("idToken")

            id_info = tokenSection.get_data_from_token(id_token)
            if(bool(id_info)):
                demo_quiz_exists = storeInDB.check_if_demo_table_exists(
                    id_info["email"])

                storeInDB.deleting_tables_with_lesser_records()

                return render_template(
                    DASHBOARD_PAGE_TEMPLATE_FILE,
                    id_token=id_token,
                    id_info=id_info,
                    demo_quiz_exists=demo_quiz_exists)

        return render_template(ERROR_PAGE_TEMPLATE_FILE)

    except BaseException:
        traceback.print_exc()


@app.route("/quiz_rules", methods=["GET", "POST"])
def quiz_rules():
    global QUIZ_RULE_PAGE_TEMPLATE_FILE, ERROR_PAGE_TEMPLATE_FILE
    question_no = 0
    difficulty_level = 1

    try:
        if(request.method == "POST"):
            id_token = request.form.get("idToken")
            topic = request.form.get("topic")

            id_info = tokenSection.get_data_from_token(id_token)
            if(bool(id_info)):
                return render_template(
                    QUIZ_RULE_PAGE_TEMPLATE_FILE,
                    id_token=id_token,
                    topic=topic,
                    question_no=question_no,
                    difficulty_level=difficulty_level)

        return render_template(ERROR_PAGE_TEMPLATE_FILE)

    except BaseException:
        traceback.print_exc()


def predict_difficulty(correct_ans, previous_ans_ticked, difficulty_level):
    if correct_ans == previous_ans_ticked and difficulty_level <= 2:
        difficulty_level += 1

    elif difficulty_level >= 2:
        difficulty_level -= 1

    return difficulty_level


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    global MCQ_QUIZ_PAGE_TEMPLATE_FILE, SUBJECTIVE_QUIZ_PAGE_TEMPLATE_FILE, ERROR_PAGE_TEMPLATE_FILE

    template_file = ""
    main_table_name = ""

    try:
        if(request.method == "POST"):
            id_token = request.form.get("idToken")
            topic = request.form.get("topic")
            previous_ans_ticked = request.form.get("answerTicked")
            previous_time_taken = request.form.get("timeTaken")

            question_no = int(request.form.get("question_no"))
            difficulty_level = int(request.form.get("difficulty_level"))
            correct_ans = request.form.get("correct_ans")

            current_question_items = request.form.get("current_question_items")
            main_table_name = request.form.get("main_table_name")

            if current_question_items is not None:
                current_question_items = ast.literal_eval(
                    current_question_items)

            if current_question_items is None:
                current_question_items = {}

            id_info = tokenSection.get_data_from_token(id_token)
            if(bool(id_info)):
                if previous_time_taken is not None:
                    current_question_items["time_taken"] = previous_time_taken

                    if question_no <= 10:
                        current_question_items["answer_ticked"] = previous_ans_ticked

                    main_table_name = storeInDB.store_in_DB(
                        main_table_name, id_info, current_question_items)

                question_no += 1

                if(topic == "Miscellaneous"):
                    question_item = quizSection.demo_questions(
                        topic, question_no)

                elif topic in ["Sports", "GK", "Technology"]:
                    difficulty_level = predict_difficulty(
                        correct_ans, previous_ans_ticked, difficulty_level)

                    question_item = quizSection.main_questions(
                        topic, question_no, difficulty_level)

                if bool(question_item) and question_no <= 10:
                    current_question_items.update(question_item)

                    if question_no < 10:
                        correct_ans = question_item["correct_answer"]
                        template_file = MCQ_QUIZ_PAGE_TEMPLATE_FILE

                    elif question_no == 10:
                        template_file = SUBJECTIVE_QUIZ_PAGE_TEMPLATE_FILE

                    return render_template(
                        template_file,
                        id_token=id_token,
                        id_info=id_info,
                        difficulty_level=difficulty_level,
                        question_no=question_no,
                        question_item=question_item,
                        correct_ans=correct_ans,
                        current_question_items=current_question_items,
                        main_table_name=main_table_name
                    )

        if question_no > 10:
            # return redirect(url_for('result_page', id_info=id_info))
            return render_template(
                "results_are_ready.html",
                id_token=id_token,
                topic=topic,
                main_table_name=main_table_name
            )

        return render_template(ERROR_PAGE_TEMPLATE_FILE)

    except BaseException:
        traceback.print_exc()


@app.route("/result", methods=["GET", "POST"])
def result_page():
    try:
        if(request.method == "POST"):
            id_token = request.form.get("idToken")
            topic = request.form.get("topic")
            main_table_name = request.form.get("main_table_name")

            id_info = tokenSection.get_data_from_token(id_token)
            if(bool(id_info)):
                question_item = storeInDB.extract_question_item_from_table(
                    main_table_name, id_info["email"], topic)

                return render_template(
                    RESULT_PAGE_TEMPLATE_FILE,
                    topic=topic,
                    question_number=question_item["question_number"],
                    difficulty_level=question_item["difficulty_level"],
                    question=question_item["question"],
                    time_taken=question_item["time_taken"],
                    answer_ticked=question_item["answer_ticked"],
                    correct_answer=question_item["correct_answer"],
                    description=question_item["description"],
                    point_scored=question_item["point_scored"],
                    total_points=question_item["total_points"])

        return render_template(ERROR_PAGE_TEMPLATE_FILE)

    except BaseException:
        traceback.print_exc()


@app.route("/already_attempted", methods=["GET", "POST"])
def already_attempted():
    try:
        if(request.method == "POST"):
            id_token = request.form.get("idToken")
            topic = request.form.get("topic")
        return render_template(
            ALREADY_ATTEMPTED_DEMO_QUIZ_TEMPLATE_FILE,
            id_token=id_token,
            topic=topic)

    except BaseException:
        traceback.print_exc()


@app.route("/statistics", methods=["GET", "POST"])
def view_statistics():
    try:
        if(request.method == "POST"):
            id_token = request.form.get("idToken")
            topic = request.form.get("topic")

            id_info = tokenSection.get_data_from_token(id_token)
            if(bool(id_info)):
                graph_items = storeInDB.extract_stats_from_table(
                    id_info["email"], topic)

                if(bool(graph_items)):
                    return render_template(
                        STATS_AVAILABLE_TEMPLATE_FILE,
                        topic=topic,
                        graph_items=graph_items)
                return render_template(
                    STATS_NOT_AVAILABLE_TEMPLATE_FILE, topic=topic)

    except BaseException:
        traceback.print_exc()


if __name__ == "__main__":
    app.run()
