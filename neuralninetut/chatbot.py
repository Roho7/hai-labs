import random
import json
import pickle
import numpy as np
import tensorflow as tf
import wikipediaapi
import pyowm
import math
import requests


import nltk
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.tree import Tree

from tensorflow.keras.models import load_model


lemmatizer = WordNetLemmatizer()
intents = json.loads(open("neuralninetut/intents.json").read())

words = pickle.load(open("neuralninetut/words.pkl", "rb"))
classes = pickle.load(open("neuralninetut/classes.pkl", "rb"))
model = load_model("neuralninetut/chatbot_model.h5")

tasks = []

api_key = "6dd7e7d54ae82988a40c243f4ed0c8fb"
owm = pyowm.OWM(api_key)


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def add_task(sentence):
    input_list = nltk.word_tokenize(sentence)
    task = ""
    time = ""
    for item in input_list:
        if item == "add":
            task = ""
        elif item == "at":
            time = " ".join(input_list[input_list.index("at") + 1 :])
            break
        else:
            task += item + " "

    task = task.strip()

    if time == "":
        return "Okay, but you need to tell me when you want to do it. Say something like: 'Add [task] at [time]"
    if task and time:
        tasks.append({"task": task, "time": time})
    else:
        print("Input format is not valid.")


def sort_tasks():
    return sorted(tasks, key=lambda x: x["time"])


def show_tasks():
    output = ""
    tasks = sort_tasks()
    if not tasks:
        return "You have nothing scheduled for today"
    for index, item in enumerate(tasks):
        if index == 0:
            message = f"You have", item["task"], "at", item["time"]
            filtered = " ".join(message)
            output += filtered
        elif index == len(tasks) - 1 and len(tasks) > 3:
            message = f"and finally", item["task"], "at", item["time"]
            filtered = ", " + " ".join(message)
            output += filtered
        else:
            message = f"and then", item["task"], "at", item["time"]
            filtered = ", " + " ".join(message)
            output += filtered
    return output


def remove_tasks(sentence):
    input_list = nltk.word_tokenize(sentence)
    bow = input_list[1]
    for item in tasks:
        if item["task"] == bow:
            tasks.remove(item)
            other_tasks = show_tasks()
            return f"{item['task']} removed from your day. {other_tasks}"
    if bow not in tasks:
        return "Item not found"


# ======== WIKIPEDIA API =========
def get_wiki(sentence):
    clean_sent = clean_up_sentence(sentence)
    if "a" in clean_sent:
        clean_sent.remove("a")
    if "an" in clean_sent:
        clean_sent.remove("an")
    pos = pos_tag(clean_sent)
    if pos[0][1] == "WP" or pos[0][0].lower() in [
        "what",
        "who",
        "where",
        "when",
        "how",
    ]:
        try:
            if "is" in clean_sent:
                is_index = clean_sent.index("is")
            elif "was" in clean_sent:
                is_index = clean_sent.index("was")
            else:
                is_index = 1
            search_query_arr = clean_sent[is_index + 1 : len(clean_sent)]
            query = " ".join(search_query_arr)
        except (ValueError, IndexError):
            print("No word found in the query.")

    wiki_wiki = wikipediaapi.Wikipedia("Zeitkonig (roho.bhattacharya@gmail.com)", "en")
    page_py = wiki_wiki.page(query)
    if not page_py.summary:
        return "Couldn't find anything. Could you try that again?"
    return f"According to wikipedia, {page_py.summary[0:400]}...To learn more you can go to {page_py.fullurl}"


# ======== WEATHER ==========
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
    return continuous_chunk or ["Nottingham"]


def get_weather(sentence):
    location = get_continuous_chunks(sentence)
    # weather_mgr = owm.weather_manager()

    try:
        # observation = weather_mgr.weather_at_place(location[0])
        # temp = observation.weather.temperature("celsius")["temp"]
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


def get_response(intents_list, intents_json, message):
    tag = intents_list[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            if i["tag"] == "add_task":
                add_task(message)
            if i["tag"] == "show_task":
                result = show_tasks()
                return result
            if i["tag"] == "remove_task":
                result = remove_tasks(message)
                return result
            if i["tag"] == "wiki":
                result = get_wiki(message)
                return result
            if i["tag"] == "weather":
                result = get_weather(message)
                return result
            result = random.choice(i["responses"])
            break
    return result


print("chatbot is running")

# while True:
#     message = input("You: ")
#     ints = predict_class(message)
#     res = get_response(ints, intents, message)
#     # clean = clean_up_sentence(message)
#     # lem = [stemmer.stem(item) for item in clean]
#     print(f"Zeitkönig:", res)


def start_bot(input):
    ints = predict_class(input)
    res = get_response(ints, intents, input)
    return res
