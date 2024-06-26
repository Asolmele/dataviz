import os
import csv
import profanity_check


def get_nb_profanity(texts):
    result = profanity_check.predict_prob(texts)
    return sum(1 for i in result if i > 0.5)


def get_author_max(authors):
    nb_author = {}
    for author in authors:
        if author in nb_author:
            nb_author[author] += 1
        else:
            nb_author[author] = 1
    max_nb = 0
    name_author = ""
    for key, value in nb_author.items():
        if value > max_nb:
            max_nb = value
            name_author = key
    return max_nb, name_author


def get_nb_x(x, texts):
    nb = 0
    for text in texts:
        nb += text.count(x)
    return nb


def get_most_used_thread(data):
    threads = {}
    for i in data:
        if i[0] == "id":
            continue
        if int(i[4]) == 0:
            threads[int(i[1])] = {"nb": 1, "data": i}
            continue
        if int(i[4]) in threads:
            threads[int(i[4])]["nb"] += 1
        else:
            print("error: thread not found")
            threads[int(i[4])] = {"nb": 1, "data": i}
    max_thread = 0
    max_thread_data = []
    for key, value in threads.items():
        if value["nb"] > max_thread:
            max_thread = value["nb"]
            max_thread_data = value["data"]
    return [max_thread_data, max_thread]


def getcsv(file):
    board_name = file.split("/")[-1].split(".")[0]
    csv_file = open(file, 'r')
    csv_reader = csv.reader(csv_file)
    data = list(csv_reader)
    authors = [i[1] for i in data if i[0] != "id"]
    texts = [i[2] for i in data if i[0] != "id"]
    nb_total = len(texts)
    nb_profanity = get_nb_profanity(texts)
    nb_author = get_author_max(authors)
    nb_link_https = get_nb_x("https://", texts)
    nb_link_http = get_nb_x("http://", texts)
    nb_word_total = sum([int(i[3]) for i in data if i[0] != "id"])
    most_used_thread = get_most_used_thread(data)
    return [board_name, nb_total, nb_profanity, nb_author[1], nb_author[0],
            nb_word_total, nb_link_https, nb_link_http, most_used_thread[0][2],
            most_used_thread[1]]


def buildresult():
    csv_file = open("results/result.csv", 'w')
    writer = csv.writer(csv_file)
    writer.writerow(["board_name", "nb_total", "nb_profanity", "author_active",
                    "nb_author_active", "nb_word_total", "nb_link_https",
                    "nb_link_http", "most_used_thread", "nb_thread_used"])
    for file in os.listdir("data"):
        print(file + " is processing")
        if file.endswith(".csv"):
            data = getcsv("data/" + file)
            writer.writerow(data)
    csv_file.close()
