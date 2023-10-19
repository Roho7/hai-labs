developers = [
    {
        "subject": "Alice",
        "verb": "work",
        "duration": 5,
        "field": "mobile apps",
        "languages": ["Java", "Kotlin"],
        "company": "TechCorp",
        "location": "at",
    },
    {
        "subject": "Bob",
        "verb": "specialize",
        "duration": 3,
        "field": "web development",
        "languages": ["JavaScript", "React"],
        "company": "WebSoft",
        "location": "with",
    },
    {
        "subject": "Charlie",
        "verb": "work",
        "duration": 7,
        "field": "mobile apps",
        "languages": ["Swift"],
        "company": "TechCorp",
        "location": "at",
    },
]


def realize(developer):
    # Morphological Inflection
    if developer["verb"] == "work" and developer["duration"] > 1:
        verb_form = "has worked"
    elif developer["verb"] == "specialise" and developer["duration"] > 1:
        verb_form = "has specialised"
    else:
        verb_form = developer["verb"]

    # Handling list of languages
    if len(developer["languages"]) > 1:
        languages = (
            ", ".join(developer["languages"][:-1])
            + " and "
            + developer["languages"][-1]
        )
    else:
        languages = developer["languages"][0]

    # Constructing the sentence based on word choice and structure
    if developer["location"] == "at":
        sentence = f"{developer['subject']} {verb_form} for {developer['duration']} years in {developer['field']} at {developer['company']} and is proficient in {languages}."
    else:
        sentence = f"{developer['subject']} {verb_form} for {developer['duration']} years in {developer['field']} with {developer['company']} and knows {languages}."

    return sentence


for developer in developers:
    bio = realize(developer)
    print(bio)
