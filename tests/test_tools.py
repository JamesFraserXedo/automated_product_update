import unittest

from Tools import *

"""
def standardise_new_lines(text):
    return text.replace("\r\n", "\n").replace("\r", "\n")

def split_on_new_line(text):
    return [i.strip() for i in standardise_new_lines(text).split("\n")]

def list_to_string(items):
    result = ''
    for item in items:
        result += '{}\r\n'.format(item)
    return result
"""


class TestTools(unittest.TestCase):

    def test_split_on_new_line(self):
        breaks = ['\n', '\r', '\r\n', '\n\r']
        for break_a in breaks:
            for break_b in breaks:
                modified_string = "alpha{}bravo{}charlie".format(break_a, break_b)
                expected = ["alpha", "bravo", "charlie"]

                self.assertEqual(split_on_new_line(modified_string), expected)

    def test_list_to_string(self):
        i = ["alpha", "bravo", "charlie"]
        expected = "alpha\nbravo\ncharlie"
        self.assertEqual(list_to_string(i), expected)
