from datetime import datetime


def get_time():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%I:%M %p")
    return f"Right now it's {formatted_time}"


def get_day():
    current_time = datetime.now()
    current_day = current_time.strftime("%A, %B %d, %Y")
    return f"Today is {current_day}"
