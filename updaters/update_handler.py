import threading

from StatusObject import StatusObject
from codec import *
from updaters.base_updater import BaseUpdater


class UpdateHandler(threading.Thread):
    def __init__(self, items, customer_code):
        threading.Thread.__init__(self)
        self.items = items
        self.customer_code = customer_code

    def run(self):
        updater = BaseUpdater(self.customer_code)
        updater.create_driver()
        updater.impersonate()

        item = self.get_next_item()
        while item:
            try:
                status_message = updater.update_product(item)
            except Exception as e:
                status_message = StatusObject(ERROR, [str(e)])

            output = "{} - {}\n".format(status_message.status, item)
            for message in status_message.messages:
                output += ("\t{}\n".format(message))

            print(output)
            item = self.get_next_item()

        updater.teardown()

    def get_next_item(self):
        if len(self.items) == 0:
            return None
        return self.items.pop()
