import csv

DEMO_MCQS_FILE = "static/CSVs/demoQuizMCQs.csv"
DEMO_SUBJECTIVE_FILE = "static/CSVs/demoQuizSubjective.csv"


def demo_questions(QUESTION_NUMBER):
    question_item = {}
    if QUESTION_NUMBER == 10:
        with open(DEMO_SUBJECTIVE_FILE) as file:
            reader = csv.DictReader(file)

            for line in reader:
                question_item["Question"] = line["Question"]
                question_item["Correct Answer"] = line["Answer"]
                break

    elif QUESTION_NUMBER < 10:
        with open(DEMO_MCQS_FILE) as file:
            reader = csv.DictReader(file)
            line_number_csv = QUESTION_NUMBER
            while(line_number_csv > 1):
                row = next(reader)
                line_number_csv = line_number_csv - 1

            for line in reader:
                if line["Difficulty Level"] in ["1", "2", "3"]:
                    if line["Difficulty Level"] == "1":
                        question_item["Difficulty Level"] = "Easy"
                        question_item["Time Limit"] = 2
                    elif line["Difficulty Level"] == "2":
                        question_item["Difficulty Level"] = "Medium"
                        question_item["Time Limit"] = 3
                    elif line["Difficulty Level"] == "3":
                        question_item["Difficulty Level"] = "Hard"
                        question_item["Time Limit"] = 5

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
