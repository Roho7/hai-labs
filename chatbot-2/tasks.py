import nltk
from cleanup import clean_up_sentence
from nltk import pos_tag
from datetime import datetime


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


def fix_time(raw):
    try:
        time_pre = datetime.strptime(raw, "%I%p")
        time = time_pre.strftime("%I:%M %p")
        return time
    except:
        right_time = input(
            f"Bot: The time wasn't quite clear, is it {raw}AM or {raw}PM?\nYou: "
        )
        if right_time.lower() == "am" or right_time.lower() == "pm":
            right_time = raw + right_time
        time_pre = datetime.strptime(right_time, "%I%p")
        time = time_pre.strftime("%I:%M %p")
        return time


def add_task(sentence):
    input_list = clean_up_sentence(sentence)
    task = ""
    time = ""
    for item in input_list:
        if item == "add":
            task = ""
        elif item == "at":
            time_raw = " ".join(input_list[input_list.index("at") + 1 :])
            time = fix_time(time_raw)
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
                    f"Bot: You already have {item['task']} at {time}, are you sure you want to add {task}?\nYou: "
                )
                if confirm.lower() in affirmations:
                    tasks.append({"task": task, "time": time})
                    return f"Okay {task} added at {time}"
                else:
                    return "Okay, try that again"
        confirm = input(
            f"Bot: You want to add {task} at {time}, is that correct?\nYou: "
        )
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
        if fix_time(time[0]) == item["time"]:
            return f"Yes, You have {item['task']} at {time[0]}"

    return f"No, you don't have anything at {time[0]}"


def shift_task(raw):
    words = nltk.word_tokenize(raw)
    tagged = pos_tag(words)
    time = None
    task = None
    for i, (word, pos) in enumerate(tagged):
        if pos == "NN":
            if i + 1 < len(tagged):
                task = [tagged[i + 1][0]]
                time = None
        elif task and pos == "CD":
            time = word
    if task:
        task = " ".join(task)

    # CHECK IF THERE IS ANOTHER TASK AT THE SAME TIME
    if fix_time(time) in [task["time"] for task in tasks]:
        existing_task = "".join(
            [task["task"] for task in tasks if task["time"] == fix_time(time)]
        )
        confirm = input(
            f"Bot: You already have {existing_task} at {time}, are you sure you want to add {task}?\nYou: "
        )
        if confirm in affirmations:
            for index, item in enumerate(tasks):
                if task == item["task"]:
                    item["time"] = fix_time(time)
                    return f"Okay, {task} shifted to {item['time']}"
        else:
            confirmation = input(
                f"Bot: Okay, do you want to add {task} at a different time?\nYou: "
            )
            if confirmation in affirmations:
                time_input = input(f"Bot: What time would you like to add it?\nYou: ")
                try:
                    for index, item in enumerate(tasks):
                        if task == item["task"]:
                            item["time"] = fix_time(time_input)
                            return f"Okay, {task} shifted to {item['time']}"
                except:
                    return f"I'm sorry, that wasn't a valid input, try adding the task again."

    for index, item in enumerate(tasks):
        if task == item["task"]:
            confirm = input(
                f"Bot: You want to shift {task} to {time}, is that correct?\nYou: "
            )
            if confirm.lower() in affirmations:
                item["time"] = fix_time(time)
                return f"{task} shifted to {item['time']}"
