import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer


lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words


def stem_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [stemmer.stem(word) for word in sentence_words]
    return sentence_words
