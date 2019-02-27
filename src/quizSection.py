#!/usr/bin/env python

import csv
import random


PATH = "static/csv"
DEMO_MCQS_FILE = PATH + "/" + "demoQuizMCQs.csv"
DEMO_SUBJECTIVE_FILE = PATH + "/" + "demoQuizSubjective.csv"

SPORTS_MCQS_FILE = PATH + "/" + "sportsMCQs.csv"
SPORTS_SUBJECTIVE_FILE = PATH + "/" + "sportsSubjective.csv"

GK_MCQS_FILE = PATH + "/" + "gkMCQs.csv"
GK_SUBJECTIVE_FILE = PATH + "/" + "gkSubjective.csv"

TECH_MCQS_FILE = PATH + "/" + "techMCQs.csv"
TECH_SUBJECTIVE_FILE = "/" + "techSubjective.csv"


MCQS_FILE = ""
SUBJECTIVE_FILE = ""

quizdata = []


def main_questions(topic, QUESTION_NUMBER, DIFFICULTY_LEVEL):
    question_item = {}
    question_item["question_number"] = QUESTION_NUMBER
    question_item["topic"] = topic

    MCQS_FILE = {
        'Sports': SPORTS_MCQS_FILE,
        'GK': GK_MCQS_FILE,
        'Technology': TECH_MCQS_FILE}.get(topic)
    SUBJECTIVE_FILE = {
        'Sports': SPORTS_SUBJECTIVE_FILE,
        'GK': GK_SUBJECTIVE_FILE,
        'Technology': TECH_SUBJECTIVE_FILE}.get(topic)

    if QUESTION_NUMBER == 10:
        with open(SUBJECTIVE_FILE) as file:
            reader = csv.DictReader(file)

            for line in reader:
                quizdata.append(line)

            random.shuffle(quizdata)
            for index in range(len(quizdata)):
                selected_question = quizdata[index]

                question_item.update(
                    add_in_question_item(
                        "-",
                        20,
                        "Subjective",
                        selected_question["Question"],
                        selected_question["Answer"],
                        "-"))
                break

    elif QUESTION_NUMBER < 10:
        with open(MCQS_FILE) as file:
            reader = csv.DictReader(file)

            for line in reader:
                quizdata.append(line)

            random.shuffle(quizdata)
            for index in range(len(quizdata)):
                if quizdata[index]['Difficulty Level'] == str(
                        DIFFICULTY_LEVEL):
                    selected_question = quizdata[index]

                    difficulty_level = {
                        '1': "Easy", '2': "Medium", '3': "Hard"}.get(
                        selected_question["Difficulty Level"])
                    time_limit = {'1': 2, '2': 3, '3': 5}.get(
                        selected_question["Difficulty Level"])

                    question_item["option_a"] = selected_question['Option A']
                    question_item["option_b"] = selected_question['Option B']
                    question_item["option_c"] = selected_question['Option C']
                    question_item["option_d"] = selected_question['Option D']
                    correct_ans = question_item["option_" +
                                                (selected_question["Correct Answer"]).lower()]

                    question_item.update(
                        add_in_question_item(
                            difficulty_level,
                            time_limit,
                            "MCQ",
                            selected_question["Question"],
                            correct_ans,
                            selected_question["Description"]))
                    break

        quizdata.clear()
    return question_item


def demo_questions(topic, QUESTION_NUMBER):
    question_item = {}
    question_item["question_number"] = QUESTION_NUMBER
    question_item["topic"] = topic

    if QUESTION_NUMBER == 10:
        with open(DEMO_SUBJECTIVE_FILE) as file:
            reader = csv.DictReader(file)

            for line in reader:
                question_item.update(
                    add_in_question_item(
                        "-",
                        20,
                        "Subjective",
                        line["Question"],
                        line["Answer"],
                        "-"))
                break

    elif QUESTION_NUMBER < 10:
        with open(DEMO_MCQS_FILE) as file:
            reader = csv.DictReader(file)
            line_number_csv = QUESTION_NUMBER
            while(line_number_csv > 1):
                row = next(reader)
                line_number_csv = line_number_csv - 1

            for line in reader:
                difficulty_level = {
                    '1': "Easy", '2': "Medium", '3': "Hard"}.get(
                    line["Difficulty Level"])
                time_limit = {
                    '1': 2, '2': 3, '3': 5}.get(
                    line["Difficulty Level"])

                question_item["option_a"] = line["Option A"]
                question_item["option_b"] = line["Option B"]
                question_item["option_c"] = line["Option C"]
                question_item["option_d"] = line["Option D"]
                correct_ans = question_item["option_" +
                                            (line["Correct Answer"]).lower()]

                question_item.update(
                    add_in_question_item(
                        difficulty_level,
                        time_limit,
                        "MCQ",
                        line["Question"],
                        correct_ans,
                        line["Description"]))
                break

    return question_item


def add_in_question_item(
        difficulty_level,
        time_limit,
        question_type,
        question,
        correct_answer,
        description):
    question_item = {}
    question_item["difficulty_level"] = difficulty_level
    question_item["time_limit"] = time_limit
    question_item["question_type"] = question_type
    question_item["question"] = question
    question_item["correct_answer"] = correct_answer
    question_item["description"] = description
    return question_item
