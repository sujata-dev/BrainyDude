import csv
f = open('demoQuizQuestions.csv')
csvreader = csv.reader(f)

first_row = next(csvreader)
for row in csvreader:
    difficulty=row[0]
    print('\n\nQ.' + row[1])
    print('\nAnswer')
    print('A.' + row[2])
    print('B.' + row[3])
    print('C.' + row[4])
    print('D.' + row[5])
    print('\nCorrect Ans ' + row[6])
    print('\nDescription ' + row[7])
