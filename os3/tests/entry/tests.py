import os
import tempfile
import unittest
from unittest import TestCase

from os3.fs.entry import Entry


class TestEntry(TestCase):
    def test_bak(self):
        name = tempfile.NamedTemporaryFile().name
        Entry(name).touch().bak()
        self.assertFalse(os.path.lexists(name))
        bak_name = '{}.bak'.format(name)
        self.assertTrue(os.path.lexists(bak_name))
        Entry(name).touch().bak()
        bak_name2 = '{}.bak0'.format(name)
        self.assertTrue(os.path.lexists(bak_name2))
        os.remove(bak_name)
        os.remove(bak_name2)

    def test_sub(self):
        self.assertEqual(Entry('/foo').sub('bar').path, '/foo/bar')


if __name__ == '__main__':
    unittest.main()
