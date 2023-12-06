import nltk
from cleanup import clean_up_sentence
from nltk import pos_tag


tasks = []
affirmations = [
    "yes",
    "ya",
    "si",
    "yesh",
    "yeah",
    "sure",
    "right",
    "correct",
    "thats right",
]


def add_task(sentence):
    input_list = clean_up_sentence(sentence)
    task = ""
    time = ""
    for item in input_list:
        if item == "add":
            task = ""
        elif item == "at":
            time = " ".join(input_list[input_list.index("at") + 1 :])
            break
        else:
            task += item + " "

    task = task.strip()

    if time == "":
        return "Okay, but you need to tell me when you want to do it. Say something like: 'Add [task] at [time]"

    if task and time:
        for i, item in enumerate(tasks):
            if time == item["time"]:
                confirm = input(
                    f"You already have {item['task']} at {time}, are you sure you want to add {task}?"
                )
                if confirm.lower() in affirmations:
                    tasks.append({"task": task, "time": time})
                    return f"Okay {task} added at {time}"
                else:
                    return "Okay, try that again"
        confirm = input(f"You want to add {task} at {time}, is that correct? ")
        if confirm.lower() in affirmations:
            tasks.append({"task": task, "time": time})
            return f"Okay {task} added at {time}"
        else:
            return "Okay, try that again"
    else:
        print("Input format is not valid.")


def remove_tasks(sentence):
    input_list = nltk.word_tokenize(sentence)
    bow = input_list[1]
    for item in tasks:
        if item["task"] == bow:
            tasks.remove(item)
            other_tasks = show_tasks()
            return f"{item['task']} removed from your day. {other_tasks}"
    if bow not in tasks:
        return "Item not found"


def sort_tasks():
    return sorted(tasks, key=lambda x: x["time"])


def show_tasks():
    output = ""
    tasks = sort_tasks()
    if not tasks:
        return "You have nothing scheduled for today"
    for index, item in enumerate(tasks):
        if index == 0:
            message = f"You have", item["task"], "at", item["time"]
            filtered = " ".join(message)
            output += filtered
        elif index == len(tasks) - 1 and len(tasks) > 3:
            message = f"and finally", item["task"], "at", item["time"]
            filtered = ", " + " ".join(message)
            output += filtered
        else:
            message = f"and then", item["task"], "at", item["time"]
            filtered = ", " + " ".join(message)
            output += filtered
    return output


def time_task(raw):
    words = nltk.word_tokenize(raw)
    tagged = pos_tag(words)
    time = [word for word, tag in tagged if tag == "CD"]
    for index, item in enumerate(tasks):
        if time[0] == item["time"]:
            return f"You have {item['task']} at {time[0]}"

    return f"No you don't have anything at {time[0]}"
