import xlrd

from codec import *
from updaters.base_updater import BaseUpdater


class BaseRunner:
    def __init__(self, filename):
        self.filename = filename
        self.sheet_rows = {}

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

    def update(self, sheet_name, loader, customer_code, collection_name):
        start_index = self.get_start_index(sheet_name)
        rows = self.sheet_rows[sheet_name]

        loader.load(collection_name, rows[start_index:])

        updater = BaseUpdater(customer_code)
        updater.create_driver()
        updater.impersonate()

        items = loader.items

        for item in items:
            try:
                status_message = updater.update_product(item)
            except Exception as e:
                status_message = (ERROR, [str(e)])

            print("{} - {}".format(status_message.status, item))
            for message in status_message.messages:
                print("\t{}".format(message))

        updater.teardown()

    def run(self):
        for sheet in self.sheets_to_update:
            self.update(
                sheet_name=sheet[SHEET_NAME],
                loader=sheet[LOADER],
                customer_code=self.customer_code,
                collection_name=sheet[COLLECTION]
            )