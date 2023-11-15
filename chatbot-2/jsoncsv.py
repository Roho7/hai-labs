import csv
import json

# Provided JSON data
json_data = [
    {
        "Document": "angry",
        "Question": ["idiot", "shut the fuck up", "you are horrible", "you suck"],
        "Answer": [
            "i am sorry, you are better than me",
            "my maker was on drugs when he built me",
            "humble yourself",
            "i am noob, yes",
            "beep boop, boop beep?",
            "what are you then eh?",
        ],
    },
    {
        "Document": "name",
        "Question": [
            "your name",
            "what is your name",
            "you name",
            "who are you",
            "what can i call you",
            "can you tell me who you are",
            "can you tell me your name",
        ],
        "Answer": [
            "I'm Zeitkönig",
            "you can call me Zeitkönig",
            "they call me Zeitkönig",
            "i am Zeitkönig",
            "i am better known as Zeitkönig",
            "i am Zeitkönig, the king of time",
            "Zeitkönig is my name",
        ],
    },
]

# Convert JSON to CSV
csv_filename = "output.csv"
csv_columns = [
    "QuestionID",
    "Question",
    "Answer",
    "Document",
]

with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=csv_columns)

    # Write header
    csv_writer.writeheader()

    # Write data
    for item in json_data:
        csv_writer.writerow(item)
