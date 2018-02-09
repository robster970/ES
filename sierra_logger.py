import datetime


class Logging:
    """Class to catch logging messages from ES"""

    def __init__(self):
        self.data = []

    @staticmethod
    def parser(module, message):
        timestamp = datetime.datetime.now()
        timestamp = timestamp.strftime("%A, %d. %B %Y %H:%M:%S.%f")
        print(timestamp + " : " + module + " : " + message)
