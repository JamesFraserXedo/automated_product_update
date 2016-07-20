import unittest
from Tools import *


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
