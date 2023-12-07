import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import random

# Load the trained model from the pickle file
with open("chatbot-4/chatbot_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Load intents data
with open("chatbot-4/intents.json", "r") as intents_file:
    dataset = json.load(intents_file)

# Extract patterns from intents for training the vectorizer
patterns = [pattern for intent in dataset["intents"] for pattern in intent["patterns"]]

# Create a TF-IDF vectorizer and fit it on the training patterns
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(patterns)


# Function to preprocess user input
def preprocess_text(text):
    return vectorizer.transform([text])


# Function to get a response from the chatbot
def get_response(user_input):
    preprocessed_input = preprocess_text(user_input)
    predicted_intent = model.predict(preprocessed_input)[0]

    for intent in dataset["intents"]:
        if intent["tag"] == predicted_intent:
            return random.choice(intent["responses"])

    return "I'm sorry, I don't understand."


# Example usage
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    response = get_response(user_input)
    print("Chatbot:", response)
