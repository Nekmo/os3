from unittest import TestCase

from os3.data.item import DataItem
from os3.data.tree import DataTree


class TestTree(TestCase):

    def test_count(self):
        count = 10
        dt = DataTree([DataItem()] * count).ls()
        self.assertEqual(dt.count(), count)

    def test_depth_count(self):
        count = 10
        sub_count = 7
        dt = DataTree([DataTree([DataItem()] * sub_count)] * count).ls(depth=True)
        self.assertEqual(dt.count(), count + (count * sub_count))
