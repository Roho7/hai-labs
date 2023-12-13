import subprocess

# DOWNLOADS WEATHER API AND WIKIPEDIA API PACKAGES
package_name = ["pyowm", "wikipedia-api"]
for package in package_name:
    subprocess.run(["pip", "insall", package])

import pandas as pd
import numpy as np
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import json
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.pipeline import make_pipeline
from nltk.stem import WordNetLemmatizer
from tasks import add_task, show_tasks, remove_tasks, time_task, shift_task, finish_task
from weather import get_weather
from name import get_username
from wiki import get_wiki
from get_time import get_time, get_day

# REMOVE AFTER FIRST RUN
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("omw-1.4")
nltk.download("averaged_perceptron_tagger")
nltk.download("maxent_ne_chunker")
nltk.download("words")

lemmatizer = WordNetLemmatizer()

intents = json.loads(open("chatbot-2/intents.json").read())

stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()


#  ============== PRE-PROCESSING ============
def text_preprocess(text):
    tokens = nltk.word_tokenize(str(text).lower())
    tokens = [
        lemmatizer.lemmatize(token)
        for token in tokens
        if token.isalpha()
        and token not in stop_words
        and not token.isdigit()
        and token not in string.punctuation
    ]
    return " ".join(tokens)


# ============== USE CLASSIFIER ===============
X_train = [
    text_preprocess(pattern)
    for intent in intents["intents"]
    for pattern in intent["patterns"]
]
y_train = [intent["tag"] for intent in intents["intents"] for _ in intent["patterns"]]

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X_train, y_train, test_size=0.25, random_state=50
)

classifiers = {
    "Multinomial Naive Bayes": MultinomialNB(),
    "Support Vector Machine": SVC(),
    "Random Forest": RandomForestClassifier(),
}

kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=50)

max_score = float("-inf")
best_classifier = None
for name, classifier in classifiers.items():
    print(name)
    pipeline = make_pipeline(TfidfVectorizer(stop_words="english"), classifier)
    scores = cross_val_score(pipeline, X_train, y_train, cv=kfold, scoring="accuracy")

    print(f"{name}:")
    print("Cross-validation scores:", scores)
    print("Average accuracy:", np.mean(scores))
    print()
    if np.mean(scores) > max_score:
        best_classifier = classifier
print("best_classifier", best_classifier)

# Creating and training the pipeline
model = make_pipeline(TfidfVectorizer(), best_classifier)
model.fit(X_train, y_train)

# Prediction on the test set
y_pred = model.predict(X_test)

# Evaluation
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print(
    "Classification Report:\n", classification_report(y_test, y_pred, zero_division=1)
)

# ======= COSINE SIMILIARITY ========
df = pd.read_csv("chatbot-2/dataset3.csv")


def get_cosine_response(input):
    df["processed_question"] = df["Question"].apply(text_preprocess)
    vectorizer = TfidfVectorizer()
    question_vectors = vectorizer.fit_transform(df["processed_question"])
    user_vector = vectorizer.transform([text_preprocess(user_input)])
    cosine_scores = cosine_similarity(user_vector, question_vectors).flatten()
    max_similarity_index = cosine_scores.argmax()
    return df.loc[max_similarity_index, "Answer"]


# ===== GENERATE RESPONSE =====
def get_response(sentence, raw):
    predicted_intent = model.predict([pre_processed])[0]
    confidence_scores = model.predict_proba([pre_processed])[0]
    confidence_for_predicted_intent = confidence_scores[
        model.classes_.tolist().index(predicted_intent)
    ]
    print(confidence_for_predicted_intent)
    if confidence_for_predicted_intent <= 0.5:
        return None
    intent_responses = {
        intent["tag"]: intent["responses"] for intent in intents["intents"]
    }
    if predicted_intent in intent_responses:
        responses = intent_responses[predicted_intent]
        response = random.choice(responses)
        if predicted_intent == "add_task":
            result = add_task(raw)
            return result
        if predicted_intent == "show_task":
            result = show_tasks()
            return result
        if predicted_intent == "time_task":
            result = time_task(raw)
            return result
        if predicted_intent == "remove_task":
            result = remove_tasks(raw)
            return result
        if predicted_intent == "shift_task":
            result = shift_task(raw)
            return result
        if predicted_intent == "finish_task":
            result = finish_task(raw)
            return result
        if predicted_intent == "wiki":
            result = get_wiki(raw)
            return result
        if predicted_intent == "weather":
            result = get_weather(raw)
            return result
        if predicted_intent == "username":
            result = get_username(raw)
            return result
        if predicted_intent == "time":
            result = get_time()
            return result
        if predicted_intent == "day":
            result = get_day()
            return result
        return response
    return None


print(
    "Zeitkonig: Hi! I'm Zeitkonig. I can help you manage your time. You can ask me to add tasks/events.\n\tTo learn more about what I can do, type 'help'."
)
while True:
    user_input = input("You: ")
    pre_processed = text_preprocess(user_input)
    response = get_response(pre_processed, user_input)
    if response != None:
        response = response
    else:
        response = get_cosine_response(user_input)
        # response = "I do not know how to respond to that. Could you come again?"
    print(f"Zeitkonig:", response)
