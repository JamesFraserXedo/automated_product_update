import os
import threading
import time
import traceback

import Utils
from StatusObject import StatusObject
from codec import *
from updaters.base_updater import BaseUpdater


class UpdateHandler(threading.Thread):
    def __init__(self, items, customer_code, logger, html_builder):
        threading.Thread.__init__(self)
        self.items = items
        self.customer_code = customer_code
        self.logger = logger
        self.html_builder = html_builder

    def run(self):
        updater = BaseUpdater(self.customer_code)
        updater.impersonate()
        item = self.get_next_item()
        while item:
            try:
                status_message = updater.update_product(item)
            except Exception as e:
                screenshot = Utils.screenshot(updater.driver, id=item.style)

                status_message = StatusObject(item.style, ERROR, [str(e), ''.join(traceback.format_exc())])
                self.logger.print(item.style)
                self.logger.error(e)
                self.logger.print('Screenshot: {}'.format(screenshot))

            #self.logger.log(product=item, status=status_message.status, messages=status_message.messages)
            self.html_builder.status_objects.append(status_message)

            print('{}: {}'.format(status_message.code, status_message.status))

            item = self.get_next_item()

        updater.teardown()

    def get_next_item(self):
        if len(self.items) == 0:
            return None
        return self.items.pop()
