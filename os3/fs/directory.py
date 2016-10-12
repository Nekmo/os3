import os

from colorama import Fore, Style

from os3.components import GradaleList
from os3.fs.entry import Entry
from os3.utils.nodes import deep_scandir


class Dir(Entry, GradaleList):
    _pre_filters = None
    __interfaces__ = ['name']
    __clone_params__ = ['path', 'deep']
    _ls = None
    _type = 'directory'

    def __init__(self, path=None, deep=None, **kwargs):
        path = path or os.getcwd()
        super(Dir, self).__init__(path)
        self.deep = deep
        self.root = kwargs.pop('root', None)
        self._pre_filters = kwargs

    def items(self):
        return []

    def _get_iter(self):
        return deep_scandir(self.path, self.deep, cls=Entry, filter=self._elem_is_valid)
        # return iter(os.listdir(self.path))

    def _prepare_next(self, elem):
        return Entry.get_node(elem.path)
        # return Node.get_node(os.path.join(self.path, elem))

    def _elem_is_valid(self, elem):
        # TODO: Hay 2 tipos de filtros: aquellos que se aplican DURANTE el listado, y aquellos que se aplican DESPUÉS.
        if elem.is_dir() and self.deep:
            # Aplicar SOLO los filtros previos a los directorios
            return elem.check_filters(**self._pre_filters or {})
        return elem.check_filters(**self._filters or {})

    def print_format(self):
        return '{Fore.BLUE}{name}{Style.RESET_ALL}'.format(name=self.name, Fore=Fore, Style=Style)

    # def __repr__(self):
    #     return pprint_list(list(self._get_iter()))

    def __repr__(self):
        return self.name


class DirPrint(Dir):
    def print_format(self):
        return GradaleList.print_format(self)

    def __repr__(self):
        return self.print_format()