import nltk
from nltk import pos_tag


name = []


def get_username(sentence):
    words = nltk.word_tokenize(sentence)
    tagged_sent = pos_tag(words)
    proper_nouns = [word for word, tag in tagged_sent if tag == "NNP"]
    question_words = [word for word, tag in tagged_sent if tag == "WP"]
    if question_words:
        print(name)
        if len(name) > 0:
            return f"Your name is {name[0]}"
        else:
            return f"you haven't told me your name"
    try:
        if proper_nouns:
            name.insert(0, proper_nouns[0])
            return f"Hi {name[0]}!"
    except:
        return f"Capitalize your name please"
