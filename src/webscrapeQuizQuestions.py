import requests
from bs4 import BeautifulSoup
import re
from random import randint
import csv


def declare_link():
    main_url = 'https://www.indiabix.com'

    sports_links_list = []
    tech_links_list = []
    gk_links_list = []

    tech_quiz_url = main_url + '/computer-science/computer-fundamentals/'
    sports_quiz_url = main_url + '/general-knowledge/sports/'
    gk_quiz_url = main_url + '/general-knowledge/basic-general-knowledge/'

    get_all_links(main_url, sports_quiz_url, sports_links_list)
    #get_all_links(main_url, tech_quiz_url, tech_links_list)
    #get_all_links(main_url, gk_quiz_url, gk_links_list)


def get_all_links(main_url, quiz_url, link_list):

    link_list.append(quiz_url)

    page = requests.get(quiz_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    find_next_pagination_link = soup.find('div', class_='mx-pager-container')
    pagination_links = [
        a.get('href') for a in find_next_pagination_link.find_all(
            'a', href=True)]

    for plink in pagination_links:
        link_list.append(main_url + plink)

    find_next_section_link = soup.find('ul', class_='ul-top-left')
    section_links = [
        a.get('href') for a in find_next_section_link.find_all(
            'a', href=True)]

    for slink in section_links:
        quiz_url = main_url + slink
        link_list.append(quiz_url)

        page = requests.get(quiz_url)
        soup = BeautifulSoup(page.text, 'html.parser')

        find_next_pagination_link = soup.find(
            'div', class_='mx-pager-container')
        pagination_links = [
            a.get('href') for a in find_next_pagination_link.find_all(
                'a', href=True)]

        for plink in pagination_links:
            link_list.append(main_url + plink)

    # print(link_list)
    scrape_web_link(link_list)


def scrape_web_link(link_list):

    i = 0
    for link in link_list:
        i = i + 1
        print(i)
        print(link)
        page = requests.get(link)
        soup = BeautifulSoup(page.text.encode('UTF-8'), 'html.parser')
        extract_question_info(soup)
    print('Done')


def extract_question_info(soup):
    for div in soup.find_all('div', class_='bix-div-container'):
        options = []
        csv_row = []
        question_item = div.find('td', class_='bix-td-qtxt')
        question_text = question_item.find('p')

        options_answer_item = div.find('td', class_='bix-td-miscell')
        answer_item = options_answer_item.find(
            'div', class_='bix-div-answer mx-none')
        answer_option = answer_item.find('span', class_='jq-hdnakqb mx-bold')
        description_item = options_answer_item.find(
            'div', class_='bix-ans-description')

        difficulty_level = randint(1, 3)
        csv_row.append(difficulty_level)

        question = question_text.get_text()
        csv_row.append(question)

        for td in options_answer_item.find_all('tr'):
            option_item = td.find(
                'td', {'class': 'bix-td-option', 'width': '99%'})
            options.append(option_item.get_text())

        for i in options:
            csv_row.append(i)

        correct_answer = answer_option.get_text()
        csv_row.append(correct_answer)

        description = description_item.get_text()
        if re.search("No answer", description):
            description = '-'

        csv_row.append(description)

        # print(csv_row)
        insert_into_csv(csv_row)


def insert_into_csv(row):
    with open('sportsQuestions.csv', 'a', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)

    csvFile.close()


if __name__ == '__main__':
    declare_link()
