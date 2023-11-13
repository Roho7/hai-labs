from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Example data
user_input = "How does this work?"
pattern = "Can you explain how this works?"

# Preprocess and vectorize the text data
vectorizer = TfidfVectorizer()
user_vector = vectorizer.fit_transform([user_input])
pattern_vector = vectorizer.transform([pattern])

# Calculate cosine similarity
cosine_score = cosine_similarity(user_vector, pattern_vector)

print("Cosine Similarity Score:", cosine_score[0][0])
