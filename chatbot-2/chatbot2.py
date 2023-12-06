import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import json
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from nltk.stem import WordNetLemmatizer
from tasks import add_task, show_tasks, remove_tasks, time_task
from weather import get_weather
from name import get_username
from wiki import get_wiki

lemmatizer = WordNetLemmatizer()


df = pd.read_csv("chatbot-2/dataset2.csv")
vocab = json.loads(open("chatbot-2/intents.json").read())
intents = json.loads(open("chatbot-2/intents.json").read())

stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()


#  ============== PRE-PROCESSING ============
def preprocess_text(text):
    tokens = nltk.word_tokenize(str(text).lower())
    tokens = [
        stemmer.stem(token)
        for token in tokens
        if token.isalpha()
        and token not in stop_words
        and not token.isdigit()
        and token not in string.punctuation
    ]
    return " ".join(tokens)


# ============== USE CLASSIFIER ===============
X_train = [
    preprocess_text(pattern)
    for intent in intents["intents"]
    for pattern in intent["patterns"]
]
y_train = [intent["tag"] for intent in intents["intents"] for _ in intent["patterns"]]

model = make_pipeline(TfidfVectorizer(), MultinomialNB())
model.fit(X_train, y_train)

# ============ USE COSINE SIMILARITY ==============
df["Question"] = df["Question"].apply(preprocess_text)
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df["Question"])


def get_similarity(pre_processed):
    user_vector = tfidf_vectorizer.transform([pre_processed])
    cosine_similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()
    return cosine_similarities


def get_score(pre_processed):
    user_vector = tfidf_vectorizer.transform([pre_processed])
    cosine_score = cosine_similarity(user_vector, tfidf_matrix).flatten()
    return cosine_score


# ===== GENERATE RESPONSE =====
def get_response(sentence, raw):
    max_similarity_index = get_similarity(sentence).argmax()
    score = get_score(sentence)
    print(score[max_similarity_index])  # getting score here between 0 - 1

    if score[max_similarity_index] > 0.7:
        response = df["Answer"][max_similarity_index]
        qdoc = df["Document"][max_similarity_index]
        if qdoc == "username":
            result = get_username(raw)
            return result
        if qdoc == "add_task":
            result = add_task(raw)
            return result
        if qdoc == "show_task":
            result = show_tasks()
            return result
        if qdoc == "get_wiki":
            result == get_wiki(raw)
            return result
        if qdoc == "time_task":
            result = time_task(raw)
            return result
        return response
    else:
        predicted_intent = model.predict([pre_processed])[0]
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
            if predicted_intent == "wiki":
                result = get_wiki(raw)
                return result
            if predicted_intent == "weather":
                result = get_weather(raw)
                return result
            if predicted_intent == "username":
                result = get_username(raw)
                return result
            return response
    return None


while True:
    user_input = input("You: ")
    pre_processed = preprocess_text(user_input)

    response = get_response(pre_processed, user_input)
    if response != None:
        response = response
    else:
        response = "what? come again?"
    print(f"Bot:", response)
