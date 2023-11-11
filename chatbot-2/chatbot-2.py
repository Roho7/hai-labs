import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
from add_task import add_task

lemmatizer = WordNetLemmatizer()


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


def get_similarity(pre_processed):
    user_vector = tfidf_vectorizer.transform([pre_processed])
    cosine_similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()
    return cosine_similarities


def get_response(sentence, raw):
    max_similarity_index = get_similarity(sentence).argmax()
    response = df["Answer"][max_similarity_index]
    qid = df["QuestionID"][max_similarity_index]
    qdoc = df["Document"][max_similarity_index]
    if qdoc == "add_task":
        result = add_task(raw)
        return f"{result}"
    return f"{format(response)},{qdoc}, {max_similarity_index}"


while True:
    user_input = input("Ask a question: ")
    pre_processed = preprocess_text(user_input)
    response = get_response(pre_processed, user_input)
    print(f"Bot:", response)
