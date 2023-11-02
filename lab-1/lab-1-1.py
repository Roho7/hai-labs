# pre-processing

import nltk, re, pprint, string
from nltk import word_tokenize, sent_tokenize
from nltk.util import ngrams
from nltk import word_tokenize, sent_tokenize

string.punctuation = string.punctuation + "’" + "-" + "‘" + "-"
string.punctuation = string.punctuation.replace(".", "")
file = open("dataset.txt", encoding="utf8 ").read()
file_nl_removed = ""

for line in file:
    line_nl_removed = line.replace("\n", " ")  # removes newline characters
    file_nl_removed += line_nl_removed  # adds filtered line to the list
file_p = "".join([char for char in file_nl_removed if char not in string.punctuation])
