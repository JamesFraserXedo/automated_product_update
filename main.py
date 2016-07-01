from loaders.other_loaders import *
from loaders.simple_loaders import *
from updaters.simple_updaters import *
from status_codes import StatusCodes

wb = xlrd.open_workbook('datasheets/ML UK PRICE LIST 2016 03.xls')


def update(spreadsheet_name, loader, updater):
    sheet = wb.sheet_by_name(spreadsheet_name)
    rows = list(sheet.get_rows())

    start_index = 0
    for row in rows:
        start_index += 1
        if str(row[0].value) == "Style":
            break

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

# update('Main', 13, MainLoader(), MainUpdater())
update('Blu', BluLoader(), BluUpdater())
# update('Voyage', VoyageLoader(), ())
# update('Angelina', AngelinaLoader(), ())
# update('Julietta', JuliettaLoader(), ())
#
# # VIZCAYA and VALENCIA sections
# update('Vizcaya', VizcayaLoader(), ())
#
# update('Sticks', SticksLoader(), ())
# update('Paparazzi Cont.', PaparazziContLoader(), ())
# update('ABM', AbmLoader(), ())
# update('Tulle Affairs', TulleAffairsLoader(), ())
# update('Affairs', AffairsLoader(), ())
# update('AF ABM', AfAbmLoader(), ())
