import csv
import os
import re


def get_link_from_text(text):
    result = []
    text = re.split(r' |\n|\r|\t', text)
    for i in text:
        if i.startswith("http"):
            result.append(i)
    return result


def getlink(file):
    csv_reader = csv.reader(open(file, 'r'))
    data = list(csv_reader)
    result = []
    for i in data:
        if i[0] == "id":
            continue
        result.extend(get_link_from_text(i[2]))
    return result


for file in os.listdir("data"):
    print(file + " is processing")
    if file.endswith(".csv"):
        data = getlink("data/" + file)
        open("link/" + file, 'w').write("\n".join(data))