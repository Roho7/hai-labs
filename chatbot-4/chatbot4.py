import numpy as np
from sklearn.utils import resample
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score

# Load dataset
data = fetch_20newsgroups(subset="all", categories=["sci.space", "comp.graphics"])
X, y = data.data, data.target

# Define classifiers to evaluate
classifiers = {
    "Multinomial Naive Bayes": MultinomialNB(),
    "Support Vector Machine": SVC(),
    "Random Forest": RandomForestClassifier(),
}

# Number of bootstrap samples - the higher it is, the more experiments will be run and the longer it will take
n_iterations = 10
size = int(len(X) * 0.50)  # 50% of the dataset

# Iterate over classifiers
for name, classifier in classifiers.items():
    scores = []
    for i in range(n_iterations):
        # Prepare bootstrap sample
        X_sample, y_sample = resample(X, y, n_samples=size)

        # Vectorize text data
        vectorizer = TfidfVectorizer(stop_words="english")
        X_sample_vec = vectorizer.fit_transform(X_sample)

        # Train classifier
        classifier.fit(X_sample_vec, y_sample)

        # Evaluate classifier
        X_test_vec = vectorizer.transform(X)  # Transform the entire dataset for testing
        y_pred = classifier.predict(X_test_vec)
        score = accuracy_score(y, y_pred)
        scores.append(score)

    # Display results
    print(f"{name}:")
    print(" Average accuracy:", np.mean(scores))
    print()
