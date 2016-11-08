from unittest import TestCase

from os3.ps.processes import Processes


class TestEntry(TestCase):
    def test_all(self):
        Processes().filter(username='nekmo')
