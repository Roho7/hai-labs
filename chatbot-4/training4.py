import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Load dataset
with open("chatbot-4/intents.json", "r") as file:
    dataset = json.load(file)

# Extract data and labels
X_train = []
y_train = []
for intent in dataset["intents"]:
    for pattern in intent["patterns"]:
        X_train.append(pattern)
        y_train.append(intent["tag"])

# Create and train the model
model = make_pipeline(TfidfVectorizer(), MultinomialNB())
model.fit(X_train, y_train)

# Save the model to a file using pickle
with open("chatbot-4/chatbot_model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

print("Model trained and saved successfully.")
