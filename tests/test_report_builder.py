import unittest

import Tools
import Utils
from StatusObject import StatusObject
from codec import *
from html_builder import HtmlBuilder


class TestTools(unittest.TestCase):

    def test_builder_ok(self):
        html_builder = HtmlBuilder("TEST_COLLECTION")

        html_builder.status_objects.append(StatusObject("1001", OK, []))
        html_builder.status_objects.append(StatusObject("1002", OK, []))
        html_builder.status_objects.append(StatusObject("1003", OK, []))
        html_builder.status_objects.append(StatusObject("1004", OK, []))
        html_builder.status_objects.append(StatusObject("1005", OK, []))

        html_builder.status_objects.append(self.get_created_object("1606", "Mori Lee Bridesmaids"))
        html_builder.status_objects.append(self.get_created_object("5473", "Sticks"))
        html_builder.status_objects.append(self.get_created_object("1259", "Angelina Faccenda"))
        html_builder.status_objects.append(self.get_created_object("3124", "Blu"))
        html_builder.status_objects.append(self.get_created_object("88081", "Something"))

        html_builder.status_objects.append(self.get_updated_object("2001", True, True, True, True, True))
        html_builder.status_objects.append(self.get_updated_object("2002", True, False, False, False, False))
        html_builder.status_objects.append(self.get_updated_object("2003", False, True, False, False, False))
        html_builder.status_objects.append(self.get_updated_object("2004", False, False, True, False, False))
        html_builder.status_objects.append(self.get_updated_object("2005", False, False, False, True, False))
        html_builder.status_objects.append(self.get_updated_object("2005", False, False, False, False, True))

        html_builder.status_objects.append(StatusObject("3001", ERROR, ['More than one product with this code (3001) found']))
        html_builder.status_objects.append(StatusObject("3002", ERROR, ['Could not select product type wedding dress']))
        s1 = StatusObject("3003", ERROR, ['Could not add colour Turquoise'])
        s1.requires_colour('Turquoise')
        html_builder.status_objects.append(s1)
        s2 = StatusObject("3004", ERROR, ['Could not add colour set Chiffon'])
        s2.requires_colour_set('Chiffon')
        html_builder.status_objects.append(s2)
        html_builder.status_objects.append(StatusObject("3005", ERROR, ['Attempted to update', 'Could not find']))

        html_builder.build()

    def get_created_object(self, code, collection):
        so = StatusObject(code=code, status=CREATED)

        so.new_name = code
        so.new_collection = collection
        so.new_image, so.all_images = Tools.get_path_to_image(code)
        so.new_size = "4-30"

        so.new_price = "£399"
        so.new_rrp = "£1000"
        so.new_colours = [
            'Red',
            'Violet',
            'ElephantTusk'
        ]
        so.new_features = None
        so.new_comments = "Available in 2 lengths\nshort\nlong"

        return so

    def get_updated_object(self, code, price, rrp, colours, comments, features):
        so = StatusObject(code=code, status=UPDATED)
        if price:
            so.old_price = 449
            so.new_price = 550

        if rrp:
            so.old_rrp = 996
            so.new_rrp = 1400

        if colours:
            so.old_colours = ['Ivory']
            so.new_colours = ['Ivory', 'Ivory/Blush']

        if features:
            so.old_features = None
            so.new_features = 'Special Lengths'

        if comments:
            so.old_comments = 'Available in 3 lengths'
            so.new_comments = 'Available in 2 lengths: short or long'

        return so