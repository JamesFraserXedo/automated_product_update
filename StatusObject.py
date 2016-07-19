from codec import *


class StatusObject:

    def __init__(self, status=OK, messages=[]):
        self.status = status
        self.messages = messages

    def add_message(self, message):
        self.messages.append(message)