import random
import json
import pickle
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn import metrics
import joblib
import h5py

import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

intents = json.loads(open("neuralninetut/intents.json").read())

words = []
classes = []
documents = []
ignore_letters = ["?", "!", ".", ","]

for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        wordList = nltk.word_tokenize(pattern)
        words.extend(wordList)
        documents.append((" ".join(wordList), intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

classes = sorted(set(classes))

pickle.dump(classes, open("neuralninetut/classes.pkl", "wb"))
pickle.dump(words, open("neuralninetut/words.pkl", "wb"))

X, y = zip(*documents)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create a pipeline with CountVectorizer and MultinomialNB
model = make_pipeline(
    CountVectorizer(
        analyzer="word", tokenizer=nltk.word_tokenize, preprocessor=lemmatizer.lemmatize
    ),
    MultinomialNB(),
)

# Train the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Print the accuracy
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

# Save the model using joblib
joblib.dump(model, "neuralninetut/chatbot_model.joblib")

# Convert the joblib file to an h5 file
with h5py.File("neuralninetut/chatbot_model.h5", "w") as hf:
    joblib.dump(model, hf)

print("Done")
