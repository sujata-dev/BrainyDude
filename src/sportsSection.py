import csv
import random

SPORTS_MCQS_FILE = "static/CSVs/sportsMCQs.csv"
SPORTS_SUBJECTIVE_FILE = "static/CSVs/sportsSubjective.csv"

GK_MCQS_FILE = "static/CSVs/gkMCQs.csv"
GK_SUBJECTIVE_FILE = "static/CSVs/gkSubjective.csv"

TECH_MCQS_FILE = "static/CSVs/techMCQs.csv"
TECH_SUBJECTIVE_FILE = ""


MCQS_FILE = ""
SUBJECTIVE_FILE = ""

quizdata = []


def sports_questions(topic, QUESTION_NUMBER, DIFFICULTY_LEVEL):
    question_item = {}
    if topic == "Sports":
        MCQS_FILE = SPORTS_MCQS_FILE
        SUBJECTIVE_FILE = SPORTS_SUBJECTIVE_FILE

    elif topic == "GK":
        MCQS_FILE = GK_MCQS_FILE
        SUBJECTIVE_FILE = GK_SUBJECTIVE_FILE

    elif topic == "Technology":
        MCQS_FILE = TECH_MCQS_FILE
        SUBJECTIVE_FILE = GK_SUBJECTIVE_FILE

    if QUESTION_NUMBER > 10:
        with open(SUBJECTIVE_FILE) as file:
            reader = csv.DictReader(file)

            for line in reader:
                quizdata.append(line)

            random.shuffle(quizdata)
            for index in range(len(quizdata)):
                selected_question = quizdata[index]
                question_item["Question"] = selected_question["Question"]
                question_item["Answer"] = selected_question["Answer"]

                break

    else:
        with open(MCQS_FILE) as file:
            reader = csv.DictReader(file)

            for line in reader:
                quizdata.append(line)

            random.shuffle(quizdata)
            for index in range(len(quizdata)):
                if quizdata[index]['Difficulty Level'] == str(
                        DIFFICULTY_LEVEL):
                    selected_question = quizdata[index]

                    if selected_question['Difficulty Level'] in [
                            "1", "2", "3"]:
                        if selected_question['Difficulty Level'] == "1":
                            question_item["Difficulty Level"] = "Easy"
                            question_item["Time Limit"] = 2

                        elif selected_question['Difficulty Level'] == "2":
                            question_item["Difficulty Level"] = "Medium"
                            question_item["Time Limit"] = 3
                        elif selected_question['Difficulty Level'] == "3":
                            question_item["Difficulty Level"] = "Hard"
                            question_item["Time Limit"] = 5

                    question_item["Question"] = selected_question['Question']
                    question_item["Option A"] = selected_question['Option A']
                    question_item["Option B"] = selected_question['Option B']
                    question_item["Option C"] = selected_question['Option C']
                    question_item["Option D"] = selected_question['Option D']
                    question_item["Correct Answer"] = question_item["Option " +
                                                                    selected_question["Correct Answer"]]
                    question_item["Description"] = line["Description"]
                    break

        quizdata.clear()
    return question_item
