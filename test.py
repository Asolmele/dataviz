import csv
import profanity_check

def testfile(file):
    nb = 0
    csv_file = open(file, 'r')
    csv_reader = csv.reader(csv_file)
    to_test = []
    for row in csv_reader:
        if row[0] == "id":
            pass
        to_test.append(row[2])
    result = profanity_check.predict(to_test)
    for key, i in enumerate(result):
        if i > 0.5:
            nb += 1
            print(to_test[key])
    return nb


result = testfile("data/vg.csv")
print(result)