from datetime import datetime


def get_current_time():

    now = datetime.now()

    return now.strftime("%I:%M:%S %p")


def get_current_date():

    now = datetime.now()

    return now.strftime("%d %B %Y")


def get_current_datetime():

    now = datetime.now()

    return now.strftime("%d %B %Y, %I:%M:%S %p")

