import nltk
from nltk import pos_tag
from nltk.tree import Tree
import requests
import math
import pyowm


api_key = "6dd7e7d54ae82988a40c243f4ed0c8fb"
owm = pyowm.OWM(api_key)


def get_continuous_chunks(text):
    tagged_sent = pos_tag(nltk.word_tokenize(text))
    for i in range(len(tagged_sent)):
        word, tag = tagged_sent[i]
        if tag == "NN" and word != "temperature" and word != "weather":
            tagged_sent[i] = (word.capitalize(), tag)
    chunked = nltk.ne_chunk(tagged_sent)
    continuous_chunk = []
    current_chunk = []
    for i in chunked:
        if type(i) == Tree:
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
        if current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue
    if continuous_chunk == []:
        return ["Nottingham"]
    return continuous_chunk


def get_weather(sentence):
    location = get_continuous_chunks(sentence)

    try:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={location[0]}&APPID={api_key}"
        ).json()
        temp = str(math.ceil(response["main"]["temp"] - 273.15))
        weather = response["weather"][0]["description"]
        main = response["weather"][0]["main"]
    except:
        return "Couldn't understand"
    if main == "Clouds":
        return f"In {location[0].capitalize()}, it is currently {temp}°C and there are {weather}"
    return f"In {location[0].capitalize()}, it is currently {temp}°C and there is {weather}"
