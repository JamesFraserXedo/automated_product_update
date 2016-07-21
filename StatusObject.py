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
        self.old_consumer_comments = None
        self.new_consumer_comments = None
        self.old_retailer_comments = None
        self.new_retailer_comments = None

        self.colours_required = []
        self.colour_sets_required = []

    def add_message(self, message):
        print(message)
        self.messages.append(message)

    def requires_colour(self, colour):
        self.colours_required.append(colour)

    def requires_colour_set(self, colour_set):
        self.colour_sets_required.append(colour_set)