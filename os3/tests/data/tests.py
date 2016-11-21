from unittest import TestCase

from os3.data.item import DataItem
from os3.data.tree import DataTree


class TestTree(TestCase):

    def test_count(self):
        dt = DataTree([DataItem()] * 10).ls()
        self.assertEqual(dt.count(), 10)
