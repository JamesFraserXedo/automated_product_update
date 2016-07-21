import os
import time
import traceback

from codec import *
from locking import get_key, unlock


class Logger:

    def __init__(self, name):
        base_dir = os.path.dirname(__file__)
        self.file_location = os.path.join(base_dir, "logs/{}_{}.log".format(name, time.strftime('%Y-%m-%d_%H-%M-%S')))

        self.tracker = {
            ERROR: [],
            CREATED: [],
            OK: [],
            UPDATED: [],
            WARNING: []
        }

    def print(self, text):
        get_key()

        with open(self.file_location, "a") as logfile:
            print(text, file=logfile)

        unlock()

    def log(self, product, status, messages):
        get_key()

        with open(self.file_location, "a") as logfile:
            print(logfile.write("{} - {}".format(status, product)), file=logfile)
            for message in messages:
                print(("\t{}".format(message)), file=logfile)
            print("", file=logfile)
        unlock()

    def error(self, e):
        get_key()

        with open(self.file_location, "a") as logfile:

            print('{}: {}'.format(type(e).__name__, str(e)), file=logfile)
            print('', file=logfile)
            print(traceback.format_exc(), file=logfile)
            print('', file=logfile)
            print('', file=logfile)

        unlock()