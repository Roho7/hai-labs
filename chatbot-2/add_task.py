from cleanup import clean_up_sentence

tasks = []


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
        tasks.append({"task": task, "time": time})
        return tasks
    else:
        print("Input format is not valid.")
