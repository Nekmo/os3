# -*- coding: utf-8 -*-
import os
import unittest
from operator import itemgetter

from os3.fs.directory import Dir
from os3.tests.base import MockTreeNode


class TestList(MockTreeNode):

    def test_list(self):
        """Comprobar que todos los archivos y directorios se estén listando correctamente en el directorio padre
        """
        self.assertEqual(set([node.name for node in Dir(self.directory).ls()]), set(self.list_dir()))

    def test_print_list(self):
        Dir(self.directory).ls().print_format()

    def test_tree(self):
        Dir(self.directory, deep=True).ls().tree_format()

    def test_subfilter(self):
        """Comprobar que los filtros sin depth estén funcionando
        """
        self.assertEqual(set([node.path for node in Dir(self.directory).ls().filter(type='d')]),
                         set(filter(os.path.isdir, self.list_dir(full_path=True))))

    def test_arg_filter(self):
        """Probar los filtros mediante argumento
        """
        self.assertEqual(set([node.path for node in Dir(self.directory).ls().filter(lambda x: x.type == 'dir')]),
                         set(filter(os.path.isdir, self.list_dir(full_path=True))))

    def test_values(self):
        """Comprobar el funcionamiento de values en listas
        """
        self.assertEqual(sorted(Dir(self.directory).ls().filter(type='f').values('name', 'path', 'size'),
                                key=itemgetter('path')),
                         sorted([{'name': os.path.split(f)[1], 'size': os.path.getsize(f), 'path': f}
                              for f in filter(os.path.isfile, self.list_dir(full_path=True))], key=itemgetter('path')))

    def test_value(self):
        """Comprobar el funcionamiento de value en listas.
        """
        self.assertEqual(set(Dir(self.directory).ls().value('path')), set(self.list_dir(full_path=True)))

    def test_sort(self):
        """Comprobar que el sort funcione.
        """
        self.assertEqual(Dir(self.directory).ls().sort('size').values('path', 'size'),
                         sorted([{'path': path, 'size': os.path.getsize(path)}

                                 for path in self.list_dir(full_path=True)], key=itemgetter('size')))


if __name__ == '__main__':
    unittest.main()
