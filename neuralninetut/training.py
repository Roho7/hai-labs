import random
import json
import pickle
import numpy as np
import tensorflow as tf

import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

intents = json.loads(open("neuralninetut/intents.json").read())

words = []
classes = []
document_list = []
ignore_letters = ["?", "!", ".", ","]

for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        wordList = nltk.word_tokenize(pattern)
        words.extend(wordList)
        document_list.append((wordList, intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

classes = sorted(set(classes))

pickle.dump(classes, open("neuralninetut/classes.pkl", "wb"))
pickle.dump(words, open("neuralninetut/words.pkl", "wb"))

training = []
outputEmpty = [0] * len(classes)

for document in document_list:
    word_patters = document[0]
    bow = []
    word_patters = [lemmatizer.lemmatize(word.lower()) for word in word_patters]
    for word in words:
        bow.append(1) if word in word_patters else bow.append(0)
    outputRow = list(outputEmpty)
    outputRow[classes.index(document[1])] = 1
    training.append(bow + outputRow)

random.shuffle(training)
training = np.array(training)

trainX = training[:, : len(words)]
trainY = training[:, len(words) :]

model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(128, input_shape=(len(trainX[0]),), activation="relu"))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(64, activation="relu"))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(len(trainY[0]), activation="softmax"))

sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

model.fit(trainX, trainY, epochs=200, batch_size=5, verbose=1)
model.save("neuralninetut/chatbot_model.h5")
print("Done")
