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

unigram = []
bigram = []
trigram = []
tokenized_text = []

sents = nltk.sent_tokenize(file_p)

for sentence in sents:
    sentence = sentence.lower()
    sequence = word_tokenize(sentence)
    for word in sequence:
        if word == ".":
            sequence.remove(word)
        else:
            unigram.append(word)
    tokenized_text.append(sequence)
    bigram.extend(list(ngrams(sequence, 2)))
    # unigram , bigram , trigram models are created
    trigram.extend(list(ngrams(sequence, 3)))

freq_uni = nltk.FreqDist(unigram)
freq_bi = nltk.FreqDist(bigram)
freq_tri = nltk.FreqDist(trigram)

print("5 most common unigrams :" + str(freq_uni.most_common(5)))
print("5 most common bigrams : " + str(freq_bi.most_common(5)))
print("5 most common trigrams : " + str(freq_tri.most_common(5)))


ngrams_all = {1: [], 2: [], 3: []}
for i in range(3):
    for each in tokenized_text:
        for j in ngrams(each, i + 1):
            ngrams_all[i + 1].append(j)

ngrams_voc = {1: set([]), 2: set([]), 3: set([])}
for i in range(3):
    for gram in ngrams_all[i + 1]:
        if gram not in ngrams_voc[i + 1]:
            ngrams_voc[i + 1].add(gram)

total_ngrams = {1: -1, 2: -1, 3: -1}


total_voc = {1: -1, 2: -1, 3: -1}
for i in range(3):
    total_ngrams[i + 1] = len(ngrams_all[i + 1])
total_voc[i + 1] = len(ngrams_voc[i + 1])

ngrams_prob = {1: [], 2: [], 3: []}
for i in range(3):
    for ngram in ngrams_voc[i + 1]:
        tlist = [ngram]
        tlist.append(ngrams_all[i + 1].count(ngram))
ngrams_prob[i + 1].append(tlist)

for i in range(3):
    for ngram in ngrams_prob[i + 1]:
        ngram[-1] = (ngram[-1] + 1) / (total_ngrams[i + 1] + total_voc[i + 1])

for i in range(3):
    ngrams_prob[i + 1] = sorted(ngrams_prob[i + 1], key=lambda x: x[1], reverse=True)

print(" Most common (1 ,2 ,3) -grams ")
print(" Most common unigrams : " + str(ngrams_prob[1][:10]))
print(" Most common bigrams : " + str(ngrams_prob[2][:10]))
print(" Most common trigrams : " + str(ngrams_prob[3][:10]))
