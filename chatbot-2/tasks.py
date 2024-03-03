import nltk
from cleanup import clean_up_sentence, stem_sentence
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
            f"Zeitkonig: The time wasn't quite clear, is it {raw}AM or {raw}PM?\nYou: "
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
    tagged = pos_tag(input_list)
    if "VBG" in [pos for (word, pos) in tagged]:
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
            time = input(f"Zeitkonig: Okay, what time would you like to add it?\nYou: ")
            time = fix_time(time)
        for i, item in enumerate(tasks):
            if time == item["time"]:
                confirm = input(
                    f"Zeitkonig: You already have {item['task']} at {time}, are you sure you want to add {task}?\nYou: "
                )
                if confirm.lower() in affirmations:
                    tasks.append({"task": task, "time": time})
                    return f"Okay {task} added at {time}"
                else:
                    return "Okay, try that again"
        confirm = input(
            f"Zeitkonig: You want to add {task} at {time}, is that correct?\nYou: "
        )
        if confirm.lower() in affirmations:
            tasks.append({"task": task, "time": time})
            return f"Okay {task} added at {time}"
        else:
            return "Okay, try that again"
    else:
        gotten_task = input("Zeitkonig: What task would you like to add?\nYou: ")
        return add_task(gotten_task)


def remove_tasks(sentence):
    if tasks == []:
        return "You have nothing in your schedule yet."
    words = nltk.word_tokenize(sentence)
    tagged = pos_tag(words)
    task = []
    for i, (word, pos) in enumerate(tagged):
        if word in ["cancel", "remove", "delete"]:
            pass
        elif word == "from":
            break
        else:
            task.append(word)
    if task:
        task = " ".join(task)
    for item in tasks:
        if stem_sentence(item["task"]) == stem_sentence(task):
            tasks.remove(item)
            other_tasks = show_tasks()
            return f"{item['task']} removed from your day. {other_tasks}"
    if task not in tasks:
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
            return f"You have {item['task']} at {time[0]}"

    return f"You don't have anything scheduled at {time[0]}"


def shift_task(raw):
    words = nltk.word_tokenize(raw)
    tagged = pos_tag(words)
    time = ""
    task = []
    for i, (word, pos) in enumerate(tagged):
        if pos == "NN" and i < 1:
            pass
        elif pos == "CD":
            time = word
            break
        elif word == "to" and i == len(tagged) - 2:
            pass
        else:
            task.append(word)
    if task:
        task = " ".join(task)

    # CHECK IF THERE IS ANOTHER TASK AT THE SAME TIME
    if fix_time(time) in [task["time"] for task in tasks]:
        existing_task = "".join(
            [task["task"] for task in tasks if task["time"] == fix_time(time)]
        )
        confirm = input(
            f"Zeitkonig: You already have {existing_task} at {time}, are you sure you want to add {task}?\nYou: "
        )
        if confirm in affirmations:
            for index, item in enumerate(tasks):
                if task == item["task"]:
                    item["time"] = fix_time(time)
                    return f"Okay, {task} shifted to {item['time']}"
        else:
            confirmation = input(
                f"Zeitkonig: Okay, do you want to add {task} at a different time?\nYou: "
            )
            if confirmation in affirmations:
                time_input = input(
                    f"Zeitkonig: What time would you like to add it?\nYou: "
                )
                try:
                    for index, item in enumerate(tasks):
                        if task == item["task"]:
                            item["time"] = fix_time(time_input)
                            return f"Okay, {task} shifted to {item['time']}"
                except:
                    return f"I'm sorry, that wasn't a valid input, try adding the task again."
            else:
                return f"Okay, try adding it again."
    else:
        for index, item in enumerate(tasks):
            if stem_sentence(task) == stem_sentence(item["task"]):
                confirm = input(
                    f"Zeitkonig: You want to shift {task} to {time}, is that correct?\nYou: "
                )
                if confirm.lower() in affirmations:
                    item["time"] = fix_time(time)
                    return f"{task} shifted to {item['time']}"
            else:
                pass
        return f"That task is not in your day."


def finish_task(raw):
    if tasks == []:
        return f"You have no tasks at the moment."
    task = input(
        f"Zeitkonig: Which task did you just complete?\n {', '.join(t['task'] for t in tasks)}\nYou: "
    )
    words = nltk.word_tokenize(raw)
    tagged = pos_tag(words)
    for i, t in enumerate(tasks):
        if stem_sentence(t["task"]) == stem_sentence(task):
            tasks.remove(t)
            return f"{task} has been completed."
    return f"That task isn't in your schedule, try that again."
