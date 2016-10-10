import os
import unittest
from operator import itemgetter

from os3.components.nodes import Dir
from os3.tests.base import MockTreeNode


class TestDirectory(MockTreeNode):
    def test_deep(self):
        self.assertEqual(set(Dir(self.directory, deep=True).value('path')), self.deep_list_dir())

    def test_not_repeated(self):
        items = Dir(self.directory, deep=True).value('path')
        self.assertEqual(len(items), len(set(items)))

    def test_max_deep(self):
        self.assertEqual(set(Dir(self.directory, deep=0).value('path')), set(self.list_dir(full_path=True)))
        self.assertNotIn(os.path.join(self.directory, 'dir01/subdir01/subsubdir01'),
                         Dir(self.directory, deep=1).value('path'))
        self.assertIn(os.path.join(self.directory, 'dir01/subdir01/subsubdir01'),
                      Dir(self.directory, deep=2).value('path'))

    def test_filters_deep(self):
        #print([x for x in Dir(self.directory, deep=True).filter(type='f')])
        pass

    def test_pre_filters_deep(self):
        print([x for x in Dir(self.directory, type='f', deep=True)])


if __name__ == '__main__':
    unittest.main()
