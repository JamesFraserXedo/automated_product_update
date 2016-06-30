import xlrd
from loaders.simple_loaders import MainLoader
from status_codes import StatusCodes
from updaters.simple_updaters import MainUpdater

wb = xlrd.open_workbook('datasheets/ML UK PRICE LIST 2016 03.xls')


def update(spreadsheet_name, start_index, loader, updater):
    sheet = wb.sheet_by_name(spreadsheet_name)
    rows = list(sheet.get_rows())

    loader.load(rows[start_index:])

    updater.create_driver()
    updater.impersonate()

    items = loader.items

    for item in items:
        try:
            status_message = updater.update_product(item)
        except Exception as e:
            status_message = {
                "status": StatusCodes.ERROR,
                "messages": e
            }
        status = status_message["status"]
        print("{} - {}".format(status, item))
        for message in status_message["messages"]:
            print("\t{}".format(message))

    updater.teardown()

update('Main', 13, MainLoader(), MainUpdater())


def update_blu():
    START_INDEX = 13

def update_voyage():
    START_INDEX = 13

def update_angelina():
    START_INDEX = 11

def update_julietta():
    START_INDEX = 11

def update_vicaya():
    START_INDEX = 13
    # Randomly puts VIZCAYA as a claim into their sheets

def update_sticks():
    START_INDEX = 14

def update_paparazzi_cont():
    START_INDEX = 14

def update_abm():
    START_INDEX = 12

def update_tulle_affairs():
    START_INDEX = 12

def update_affairs():
    START_INDEX = 12

def update_af_abm():
    START_INDEX = 11