import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv("chatbot-2/dataset.csv")


nltk.download("stopwords")
stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()


# preprocess the text
def preprocess_text(text):
    tokens = nltk.word_tokenize(text.lower())
    tokens = [
        stemmer.stem(token)
        for token in tokens
        if token.isalpha() and token not in stop_words
    ]
    return " ".join(tokens)


df["Question"] = df["Question"].apply(preprocess_text)


tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df["Question"])


user_input = input("Ask a question: ")
user_input = preprocess_text(user_input)
user_vector = tfidf_vectorizer.transform([user_input])


cosine_similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()
max_similarity_index = cosine_similarities.argmax()
response = df["Answer"][max_similarity_index]

print("Bot: {}".format(response))
