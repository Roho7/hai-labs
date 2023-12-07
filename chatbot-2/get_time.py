from datetime import datetime


def get_time():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%I:%M %p")
    return formatted_time
