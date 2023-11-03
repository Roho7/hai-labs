import random
import json
import pickle
import numpy as np
import tensorflow as tf

import nltk
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open("neuralninetut/intents.json").read())

words = pickle.load(open("neuralninetut/words.pkl", "rb"))
classes = pickle.load(open("neuralninetut/classes.pkl", "rb"))
model = load_model("neuralninetut/chatbot_model.h5")

tasks = []


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

    if task and time:
        tasks.append({"task": task, "time": time})
    else:
        print("Input format is not valid.")


def sort_tasks():
    return sorted(tasks, key=lambda x: x["time"])


def show_tasks():
    output = ""
    tasks = sort_tasks()
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
            result = random.choice(i["responses"])
            break
    return result


print("chatbot is running")

while True:
    message = input("You: ")
    ints = predict_class(message)
    res = get_response(ints, intents, message)
    print(f"Zeitkönig:", res)
