import os
import time

from codec import *
from html_builder import HtmlBuilder
from locking import get_key, unlock


class Logger:

    def __init__(self, name):
        base_dir = os.path.dirname(__file__)
        self.html_file = os.path.join(base_dir, "reports/{}_{}.html".format(name, time.strftime('%Y-%m-%d_%H-%M-%S')))
        self.file_location = os.path.join(base_dir, "logs/{}_{}.log".format(name, time.strftime('%Y-%m-%d_%H-%M-%S')))

        self.tracker = {
            ERROR: [],
            NEEDS_CREATED: [],
            OK: [],
            UPDATED: [],
            WARNING: []
        }

    def log(self, product, status, messages):
        get_key()

        with open(self.file_location, "a") as logfile:
            print(logfile.write("{} - {}".format(status, product)), file=logfile)
            for message in messages:
                print(("\t{}".format(message)), file=logfile)
            print("", file=logfile)
        unlock()

        self.tracker[status].append(
            {
                "product": product,
                "messages": messages
            }
        )

    def dump_to_html(self):
        builder = HtmlBuilder(self.tracker, self.html_file)
        builder.build()
