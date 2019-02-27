#!/usr/bin/env python

import sqlite3
from sqlite3 import Error
import spacy
import time
import re


DATABASE = "brainydude.db"
SQL_CREATE_TABLE = """create table `{0}`(
                        question_number     integer primary key,
                        difficulty_level    text,
                        question            text,
                        time_taken          integer,
                        answer_ticked       text,
                        correct_answer      text,
                        description         text,
                        points_scored       integer
                    );"""

POINTS = 0
NLP = spacy.load('en_core_web_sm')


# drop the table if the quiz is left midway, (error or time out)
def store_in_DB(id_info, CURRENT_QUESTION_ITEMS):
    global POINTS
    global SQL_CREATE_TABLE
    email_id = id_info["email"]
    POINTS = 0

    if CURRENT_QUESTION_ITEMS["topic"] == "Miscellaneous":
        table_prefix = "demo"

    elif topic in ["Sports", "GK", "Technology"]:
        table_prefix = int(time.time()) + "main" + topic

    table_name = table_prefix + "_table_" + email_id

    conn = create_connection()
    cur = conn.cursor()

    if CURRENT_QUESTION_ITEMS["question_number"] == 1:
        cur.execute("drop table if exists `%s`;" % table_name)
        create_table(cur, SQL_CREATE_TABLE.format(table_name))

    time_taken = (
        float(
            CURRENT_QUESTION_ITEMS["time_taken"]) / CURRENT_QUESTION_ITEMS["time_limit"]) * 100
    time_taken = str(round(time_taken, 2)) + "%"
    points_scored = get_score(CURRENT_QUESTION_ITEMS)

    with conn:
        q_items = (
            CURRENT_QUESTION_ITEMS["question_number"],
            CURRENT_QUESTION_ITEMS["difficulty_level"],
            CURRENT_QUESTION_ITEMS["question"],
            time_taken,
            CURRENT_QUESTION_ITEMS["answer_ticked"],
            CURRENT_QUESTION_ITEMS["correct_answer"],
            CURRENT_QUESTION_ITEMS["description"],
            points_scored
        )
        insert_data(cur, table_name, q_items)

    # CURRENT_QUESTION_ITEMS["topic"]
    conn.commit()
    conn.close()


def create_connection():
    global DATABASE

    try:
        conn = sqlite3.connect(DATABASE)
        if conn is not None:
            return conn

    except Error as e:
        print(e)

    print("Error! Cannot create database connection")
    return Error


def create_table(cur, SQL_CREATE_TABLE):
    try:
        cur.execute(SQL_CREATE_TABLE)
    except Error as e:
        print(e)


def insert_data(cur, table_name, q_items):
    sql_insert_statement = '''insert into `{0}`(
                                question_number,
                                difficulty_level,
                                question,
                                time_taken,
                                answer_ticked,
                                correct_answer,
                                description,
                                points_scored
                            )
                            values(?, ?, ?, ?, ?, ?, ?, ?)'''

    cur.execute(sql_insert_statement.format(table_name), q_items)
    return cur.lastrowid


def get_score(CURRENT_QUESTION_ITEMS):
    global POINTS
    if(CURRENT_QUESTION_ITEMS["question_number"] < 10):
        if(CURRENT_QUESTION_ITEMS["answer_ticked"] == CURRENT_QUESTION_ITEMS["correct_answer"]):
            POINTS = {"Easy": 2, "Medium": 3, "Hard": 5}.get(
                CURRENT_QUESTION_ITEMS["difficulty_level"])

    elif(CURRENT_QUESTION_ITEMS["question_number"] == 10):
        POINTS = find_accuracy_spacy(CURRENT_QUESTION_ITEMS)

    return POINTS


def find_accuracy_spacy(CURRENT_QUESTION_ITEMS):
    global NLP

    answer_ticked_doc = NLP(CURRENT_QUESTION_ITEMS["answer_ticked"])
    correct_answer_doc = NLP(CURRENT_QUESTION_ITEMS["correct_answer"])
    similarity = answer_ticked_doc.similarity(correct_answer_doc)

    return int(similarity * 10)


def check_if_demo_table_exists(email_id):
    conn = create_connection()
    cur = conn.cursor()
    exists = False
    for table_name in cur.execute(
        "select name from sqlite_master where type='table' AND name like \"demo%" +
        email_id +
            "\";"):
        for count in cur.execute(
            "select COUNT(*) from '" +
            table_name[0] +
                "';"):
            if(count[0] < 10):
                print("deleting")
                cur.execute("drop table '" + table_name[0] + "';")
            elif(count[0] == 10):
                print(count[0])
                exists = True

    conn.close()
    return exists


def extract_question_item_from_demo_table(email_id):
    question_item = {}
    question_item["question_number"] = []
    question_item["difficulty_level"] = []
    question_item["question"] = []
    question_item["time_taken"] = []
    question_item["answer_ticked"] = []
    question_item["correct_answer"] = []
    question_item["description"] = []
    question_item["point_scored"] = []

    conn = create_connection()
    cur = conn.cursor()
    for table_name in cur.execute(
        "select name from sqlite_master where type='table' AND name like \"demo%" +
        email_id +
            "\";"):
        for item in cur.execute("select * from '" + table_name[0] + "';"):
            question_item["question_number"].append(item[0])
            question_item["difficulty_level"].append(item[1])
            question_item["question"].append(item[2])
            question_item["time_taken"].append(item[3])
            question_item["answer_ticked"].append(item[4])
            question_item["correct_answer"].append(item[5])
            question_item["description"].append(item[6])
            question_item["point_scored"].append(item[7])

    question_item["total_points"] = sum(question_item["point_scored"])

    return question_item
