import os

import time

from codec import *


class HtmlBuilder:

    def __init__(self, collection):
        self.building = None
        self.status_objects = []
        base_dir = os.path.dirname(__file__)
        self.html_file = os.path.join(base_dir, "reports/{}_{}.html".format(collection, time.strftime('%Y-%m-%d_%H-%M-%S')))
        self.collection = collection

    def build(self):
        try:
            self.building = open(self.html_file, "a")

            print("<html>", file=self.building)
            print("<h1>{}</h1>".format(self.collection), file=self.building)

            for key in [ERROR, CREATED, UPDATED, OK]:
                records = []
                for obj in self.status_objects:
                    if obj.status == key:
                        records.append(obj)

                if len(records) > 0:

                    self.write_header(key, len(records))
                    self.start_table(key)

                    for record in records:
                        self.add_record(record)

                    self.end_table()

            print("</html>", file=self.building)
        finally:
            self.building.close()

    def write_header(self, header, size):
        print("<h2>{} ({})</h2>".format(header, size), file=self.building)

    def start_table(self, key):
        print('<table border="1">', file=self.building)
        print('<tr>', file=self.building)

        self.print_table_column_header('Style')

        if key == OK:
            columns = [
                'Status'
            ]

        elif key == CREATED:
            columns = [
                'Name',
                'Collection',
                'Image',
                'All Images',
                'Size',
                'Price',
                'RRP',
                'Colours',
                'Comments',
                'Features'
            ]

        elif key == UPDATED:
            columns = [
                'Price',
                'RRP',
                'Colours',
                'Comments',
                'Features'
            ]

        elif key == ERROR:
            columns = [
                'Messages'
            ]

        for column in columns:
            self.print_table_column_header(column)
        print('</tr>', file=self.building)

    def end_table(self):
        # print("</ul>", file=self.building)
        print('</table>', file=self.building)

    def add_record(self, record):
        key = record.status

        print('<tr>', file=self.building)
        print('<td>{}</td>'.format(record.code), file=self.building)
        if key == OK:
            print('<td>OK</td>', file=self.building)

        elif key == CREATED:
            print('<td>{}</td>'.format(record.new_name), file=self.building)
            print('<td>{}</td>'.format(record.new_collection), file=self.building)
            print('<td>{}</td>'.format(record.new_image), file=self.building)

            print('<td><ul>', file=self.building)
            for image in record.all_images:
                print('<li>{}</li>'.format(image), file=self.building)
            print('</ul></td>', file=self.building)

            print('<td>{}</td>'.format(record.new_size), file=self.building)
            print('<td>{}</td>'.format(record.new_price), file=self.building)
            print('<td>{}</td>'.format(record.new_rrp), file=self.building)

            print('<td><ul>', file=self.building)
            for colour in record.new_colours:
                print('<li>{}</li>'.format(colour), file=self.building)
            print('</ul></td>', file=self.building)

            print('<td>{}</td>'.format(record.new_comments), file=self.building)
            print('<td>{}</td>'.format(record.new_features), file=self.building)

        elif key == UPDATED:
            print('<td>', file=self.building)
            if record.old_price or record.new_price:
                print('From: {}<br>To: {}'.format(record.old_price, record.new_price), file=self.building)
            print('</td>', file=self.building)

            print('<td>', file=self.building)
            if record.old_rrp or record.new_rrp:
                print('From: {}<br>To: {}'.format(record.old_rrp, record.new_rrp), file=self.building)
            print('</td>', file=self.building)

            print('<td>', file=self.building)
            if record.old_colours or record.new_colours:
                print('From: {}<br>To: {}'.format(record.old_colours, record.new_colours), file=self.building)
            print('</td>', file=self.building)

            print('<td>', file=self.building)
            if record.old_comments or record.new_comments:
                print('From: {}<br>To: {}'.format(record.old_comments, record.new_comments), file=self.building)
            print('</td>', file=self.building)

            print('<td>', file=self.building)
            if record.old_features or record.new_features:

                print('From: {}<br>To: {}'.format(record.old_features, record.new_features), file=self.building)
            print('</td>', file=self.building)
        elif key == ERROR:
            print('<td><ul>', file=self.building)
            for message in record.messages:
                print('<li>{}</li>'.format(message), file=self.building)
            print('</ul></td>', file=self.building)

        print('</tr>', file=self.building)

    def print_table_column_header(self, name):
        print('<td><b>{}</b></td>'.format(name), file=self.building)
