from codec import *


class StatusObject:

    def __init__(self, code, status=OK, messages=[]):
        self.code = code

        self.status = status
        self.messages = messages

        self.new_name = None
        self.new_collection = None
        self.new_image = None
        self.new_size = None
        self.all_images = None

        self.old_price = None
        self.new_price = None
        self.old_rrp = None
        self.new_rrp = None
        self.old_colours = None
        self.new_colours = None
        self.old_features = None
        self.new_features = None
        self.old_comments = None
        self.new_comments = None

    def add_message(self, message):
        self.messages.append(message)