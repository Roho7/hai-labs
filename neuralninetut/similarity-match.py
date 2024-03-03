import os
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

document_path = "/Users/roho7/Documents/MAIN/HCI/HAI/neuralninetut/dataset.csv"

# corpus = {}
# for file in os.listdir(document_path):
#     filepath = document_path + os.sep + file
#     with open(filepath, encoding="utf8", errors="ignore", mode="r") as document:
#         content = document.read()
#         document_id = file
#         corpus[document_id] = content


def calculate_cosine_similarity(csv_file, column1, column2):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Check if the specified columns exist in the DataFrame
        if column1 not in df.columns or column2 not in df.columns:
            raise ValueError("Specified columns do not exist in the CSV file")

        # Get the values of the specified columns
        values1 = df[column1].values
        values2 = df[column2].values

        # Calculate the cosine similarity
        similarity = cosine_similarity([values1], [values2])[0][0]

        return similarity
    except (FileNotFoundError, ValueError) as e:
        # Log the error
        print(f"Error: {e}")
        return None


stop = False
while not stop:
    query = input(" Enter your query , or STOP to quit , and press return : ")
    if query == " STOP ":
        stop = True
    else:
        print(f"You are searching for {query}")
        print(calculate_cosine_similarity(document_path, "Question", "Answer"))
