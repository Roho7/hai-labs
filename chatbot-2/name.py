import nltk
from nltk import pos_tag


def get_username(sentence):
    words = nltk.word_tokenize(sentence)
    tagged_sent = pos_tag(words)
    proper_nouns = [word for word, tag in tagged_sent if tag == "NNP"]
    # for w, tag in tagged_sent:
    #     if tag == "NNP":
    #         return w
    return f"Hi {proper_nouns[0]}!"
