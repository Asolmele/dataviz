import csv

import pathlib

res_dir = str(pathlib.Path(__file__).parent.parent.resolve().joinpath("results"))
csv_reader = csv.reader(open(res_dir + "/result.csv", 'r'))

data = list(csv_reader)


INDEX_NAME = 0
INDEX_NB_TOTAL = 1
INDEX_NB_PROFANITY = 2
INDEX_AUTHOR_ACTIVE = 3
INDEX_NB_AUTHOR_ACTIVE = 4
INDEX_NB_WORD_TOTAL = 5
INDEX_NB_LINK_HTTPS = 6
INDEX_NB_LINK_HTTP = 7


def get_ratio(list_1, list_2):
    return [list_1[i] / list_2[i] for i in range(len(list_1))]


def get_max(list_1):
    max_value = 0
    index = 0
    for i in range(len(list_1)):
        if list_1[i] > max_value:
            max_value = list_1[i]
            index = i
    return max_value, index


def get_something(data, index):
    l_get = [int(i[index]) for i in data[1:] if i[0] != "id"]
    return l_get


def get_something_ratio(data, l1_index, l2_index):
    l1 = get_something(data, l1_index)
    l2 = get_something(data, l2_index)
    return get_ratio(l1, l2)


def get_name(data, l1_index, l2_index):
    ratio = get_something_ratio(data, l1_index, l2_index)
    index = get_max(ratio)[1]
    return data[index + 1][INDEX_NAME]


print("The board with the highest ratio of profanity is: " + get_name(data, INDEX_NB_PROFANITY, INDEX_NB_TOTAL))
print("The board with the highest ratio of word total is: " + get_name(data, INDEX_NB_WORD_TOTAL, INDEX_NB_TOTAL))
print("The board with the highest ratio of link https is: " + get_name(data, INDEX_NB_LINK_HTTPS, INDEX_NB_TOTAL))
print("The board with the highest ratio of link http is: " + get_name(data, INDEX_NB_LINK_HTTP, INDEX_NB_TOTAL))
