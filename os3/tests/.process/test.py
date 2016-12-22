from unittest import TestCase

from os3.ps.processes import Processes


class TestEntry(TestCase):
    def test_filter(self):
        Processes().filter(username='nekmo')

    def test_print(self):
        Processes().print_format()

    def test_tree(self):
        Processes().tree_format()
