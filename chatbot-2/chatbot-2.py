import pandas as pd
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
from tasks import add_task, show_tasks, remove_tasks
from name import get_username

lemmatizer = WordNetLemmatizer()


df = pd.read_csv("chatbot-2/dataset.csv")
vocab = json.loads(open("chatbot-2/intents.json").read())
intents = json.loads(open("chatbot-2/intents.json").read())

stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()


# preprocess the text
def preprocess_text(text):
    tokens = nltk.word_tokenize(str(text).lower())
    tokens = [
        stemmer.stem(token)
        for token in tokens
        if token.isalpha() and token not in stop_words
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

# ========= USE COSINE SIMILARITY ==============
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


def get_response(sentence, raw):
    max_similarity_index = get_similarity(sentence).argmax()
    score = get_score(sentence)
    print(score[max_similarity_index])  # getting score here between 0 - 1

    if score[max_similarity_index] > 0.0:
        response = df["Answer"][max_similarity_index]
        qdoc = df["Document"][max_similarity_index]
        if qdoc == "add_task":
            result = add_task(raw)
            return f"{result}"
        if qdoc == "show_task":
            result = show_tasks()
            return result
        if qdoc == "remove_tasks":
            result = remove_tasks(raw)
            return result
        if qdoc == "store_name":
            result = get_username(raw)
            return result
        return response
    return None


while True:
    user_input = input("Ask a question: ")
    pre_processed = preprocess_text(user_input)
    predicted_intent = model.predict([pre_processed])[0]

    # Generate Response Based on Predicted Intent
    intent_responses = {
        intent["tag"]: intent["responses"] for intent in intents["intents"]
    }

    cosine_response = get_response(pre_processed, user_input)
    if cosine_response != None:
        response = cosine_response + "cos"
    elif predicted_intent in intent_responses:
        responses = intent_responses[predicted_intent]
        response = random.choice(responses) + "clas"
    else:
        response = "what? come again?"
    print(f"Bot:", response)
