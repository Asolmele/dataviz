import csv
import os
import re


def get_link_from_text(text):
    result = []
    text = re.split(r' |\n|\r|\t', text)
    for i in text:
        if i.startswith("http://") or i.startswith("https://"):
            result.append(i)
    return result


def getlink(file):
    csv_reader = csv.reader(open(file, 'r'))
    data = list(csv_reader)
    result = {}
    all_links = []
    for i in data:
        if i[0] == "id":
            continue
        links = get_link_from_text(i[2])
        all_links.extend(links)
        for x in links:
            x = x.split("/")[2]
            if x in result.keys():
                result[x] += 1
            else:
                result[x] = 1

    def sort_by_value(item):
        return item[1]
    result = dict(sorted(result.items(), key=sort_by_value, reverse=True))
    return [result.items(), all_links]


def buildlink():
    for file in os.listdir("data"):
        print(file + " is processing")
        if file.endswith(".csv"):
            data = getlink("data/" + file)
            open("results/link/all/" + file, 'w').write("\n".join(data[1]))
            count_file = csv.writer(open("results/link/count/" + file, 'w'))
            count_file.writerow(["link", "count"])
            for i in data[0]:
                count_file.writerow(i)
