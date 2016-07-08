import copy
import threading

import xlrd

from credentials import Credentials
from codec import *
from updaters.base_updater import BaseUpdater
from updaters.update_handler import UpdateHandler


class BaseRunner:
    def __init__(self, filename):
        self.filename = filename
        self.sheet_rows = {}
        self.items = []

        workbook = xlrd.open_workbook(self.filename)
        print(type(workbook), workbook)
        for sheet_name in workbook.sheet_names():
            self.sheet_rows[sheet_name] = list(workbook.sheet_by_name(sheet_name).get_rows())

    def get_start_index(self, sheet_name):
        start_index = 0
        rows = self.sheet_rows[sheet_name]
        for row in rows:
            start_index += 1
            if str(row[0].value) == "Style":
                return start_index
        raise Exception("Could not determine start index for sheet '{}'".format(sheet_name))

    def update(self, sheet_name, loader, customer_code, collection_name, product_type):
        start_index = self.get_start_index(sheet_name)
        rows = self.sheet_rows[sheet_name]

        loader.load(collection_name, rows[start_index:], product_type)

        updaters = []
        self.items = copy.deepcopy(loader.items)

        for x in range(Credentials.num_threads):
            t = UpdateHandler(self.items, customer_code)
            updaters.append(t)
            t.start()

        for updater in updaters:
            updater.join()

    def run(self):
        for sheet in self.sheets_to_update:
            self.update(
                sheet_name=sheet[SHEET_NAME],
                loader=sheet[LOADER],
                customer_code=self.customer_code,
                collection_name=sheet[COLLECTION],
                product_type=sheet[PRODUCT_TYPE]
            )