import nltk

nltk.download("punkt")

from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer


def tokenize(sentence):
    return nltk.word_tokenize(sentence)


def stem(w):
    return stemmer.stem(w.lower())


def bag_of_words(tokenized_sentence, all_words):
    pass
