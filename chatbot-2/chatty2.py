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

lemmatizer = nltk.WordNetLemmatizer()

df = pd.read_csv("chatbot-2/dataset2.csv")
intents = json.loads(open("chatbot-2/intents.json").read())

stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()


# ============== PRE-PROCESSING ============
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

# ============ USE COSINE SIMILARITY ==============
df["Question"] = df["Question"].apply(preprocess_text)
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df["Question"])


def get_similarity(pre_processed):
    user_vector = tfidf_vectorizer.transform([pre_processed])
    cosine_similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()
    return cosine_similarities


def get_response(sentence, raw):
    predicted_intent = model.predict([preprocess_text(sentence)])[0]

    if predicted_intent == "time_task":
        # Handle time-related tasks
        # You might want to integrate a proper time management system here
        # For now, let's just provide a placeholder response
        return "Placeholder response for time-related tasks"

    max_similarity_index = get_similarity(preprocess_text(sentence)).argmax()
    score = get_similarity(preprocess_text(sentence))[max_similarity_index]

    if score > 0.7:
        response = df["Answer"][max_similarity_index]
        return response
    else:
        intent_responses = {
            intent["tag"]: intent["responses"] for intent in intents["intents"]
        }
        responses = intent_responses.get(
            predicted_intent, ["I'm not sure how to respond."]
        )
        return random.choice(responses)


# Example usage:
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    response = get_response(user_input, user_input)
    print(f"Bot: {response}")
